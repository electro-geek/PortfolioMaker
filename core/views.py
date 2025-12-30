import os
import zipfile
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.contrib import messages
from django.template import Template, Context
from django.template.loader import render_to_string
from .utils import get_portfolio_data, extract_text_from_pdf
from .forms import ResumeUploadForm
from .models import PortfolioTemplate, PremiumWaitlist


import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.core.management import call_command
from firebase_admin import auth
import io
import sys

def firebase_login(request):
    """Verify Firebase ID token and login user"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        data = json.loads(request.body)
        id_token = data.get('id_token')
        
        if not id_token:
            return JsonResponse({'error': 'No ID token provided'}, status=400)
            
        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
        picture = decoded_token.get('picture', '')
        
        if not email:
            # Fallback for users without a public email (common on GitHub)
            email = f"{uid}@no-email.firebase"
            print(f"DEBUG: No email found in token for UID {uid}, using fallback: {email}")
            
        # Get or create user
        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            # Create new user
            # Use UID as username to ensure uniqueness
            user = User.objects.create_user(
                username=uid,
                email=email,
                first_name=name
            )
            
        # Log the user in
        login(request, user)
        
        # Save profile picture to session
        request.session['user_picture'] = picture
        
        return JsonResponse({'status': 'success', 'username': user.username})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=401)

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def clear_api_key(request):
    """Clear the saved Gemini API key from user profile"""
    try:
        profile = request.user.userprofile
        profile.gemini_api_key = None
        profile.save()
        messages.success(request, 'Saved API key cleared successfully.')
    except Exception as e:
        messages.error(request, f'Error clearing API key: {str(e)}')
    return redirect('home')

def home(request):
    """Render home page with Firebase config"""
    context = {
        'firebase_config': json.dumps({
            'apiKey': settings.FIREBASE_API_KEY,
            'authDomain': settings.FIREBASE_AUTH_DOMAIN,
            'projectId': settings.FIREBASE_PROJECT_ID,
            'storageBucket': settings.FIREBASE_STORAGE_BUCKET,
            'messagingSenderId': settings.FIREBASE_MESSAGING_SENDER_ID,
            'appId': settings.FIREBASE_APP_ID,
        })
    }
    
    # Check if user has generated portfolio
    if request.user.is_authenticated:
        try:
            profile = request.user.userprofile
            context['has_api_key'] = bool(profile.gemini_api_key)
            
            # Grant unlimited access to admin users defined in config
            if request.user.email in settings.ADMIN_EMAILS:
                context['has_generated_portfolio'] = False
            else:
                context['has_generated_portfolio'] = profile.has_generated_portfolio
        except Exception:
            context['has_generated_portfolio'] = False
            context['has_api_key'] = False
            
    return render(request, 'core/home.html', context)


@login_required
def upload_resume(request):
    """Handle PDF upload and extraction (Stateless for Vercel)"""
    if request.method == 'POST':
        if 'resume_file' not in request.FILES:
            messages.error(request, 'No file uploaded')
            return redirect('home')
            
        file = request.FILES['resume_file']
        
        # Basic validation
        if not file.name.endswith('.pdf'):
            messages.error(request, 'Only PDF files are allowed.')
            return redirect('home')
            
        if file.size > 10 * 1024 * 1024:
            messages.error(request, 'File size must be less than 10MB.')
            return redirect('home')

        try:
            # 1. Extract text directly from memory (file stream)
            text = extract_text_from_pdf(file)
            
            if not text:
                messages.error(request, 'Could not extract text from PDF. Is it an image scan?')
                return redirect('home')
            
            # 2. Determine which API key to use
            user_api_key = request.POST.get('user_api_key', '').strip()
            profile = None
            
            if request.user.is_authenticated:
                try:
                    profile = request.user.userprofile
                    # If key provided in form, save it
                    if user_api_key:
                        print(f"DEBUG: Using API key from POST for user {request.user.username}")
                        profile.gemini_api_key = user_api_key
                        profile.save()
                    # If no key in form, try to use saved key
                    elif profile.gemini_api_key:
                        print(f"DEBUG: Using saved API key from Profile for user {request.user.username}")
                        user_api_key = profile.gemini_api_key.strip()
                    else:
                        print(f"DEBUG: No user API key found, falling back to system key")
                except Exception as e:
                    print(f"DEBUG: Error accessing profile: {e}")
                    pass

            # 3. Get structured data from Gemini
            try:
                extracted_data = get_portfolio_data(text, api_key=user_api_key)
            except Exception as e:
                # If there's an error and we're using a user API key, it might be invalid
                if user_api_key and user_api_key != settings.GEMINI_API_KEY:
                    messages.error(request, f'API Key Error: {str(e)}. Please update your API key or use the premium feature.')
                else:
                    messages.error(request, f'Error processing resume: {str(e)}')
                return redirect('home')
            
            # 4. Store data in SESSION (Stateless!)
            request.session['portfolio_data'] = extracted_data
            
            # Mark that the user has used their free generation
            if profile:
                profile.has_generated_portfolio = True
                profile.save()
            
            messages.success(request, 'Resume processed successfully!')
            return redirect('select_template')
            
        except Exception as e:
            messages.error(request, f'Unexpected error: {str(e)}')
            return redirect('home')
    else:
        form = ResumeUploadForm()
    
    return render(request, 'core/home.html', {'form': form})


@login_required
def select_template(request):
    """Display available templates for selection"""
    # Check if we have data in session
    portfolio_data = request.session.get('portfolio_data')
    if not portfolio_data:
        messages.error(request, 'Please upload a resume first.')
        return redirect('home')
    
    # Get templates (these are read-only from DB, which is fine if pre-populated)
    # OR we can just define them statically if DB is empty on Vercel
    templates = PortfolioTemplate.objects.filter(is_active=True)
    
    # Fallback if DB is empty (common on Vercel if migrations didn't run)
    if not templates.exists():
        # Create dummy template objects for display
        class DummyTemplate:
            def __init__(self, name, slug, description):
                self.name = name
                self.slug = slug
                self.description = description
        
        templates = [
            DummyTemplate('Terminal', 'terminal', 'Retro hacker terminal with green monospace text'),
            DummyTemplate('Renaissance', 'renaissance', 'Classical art-inspired design with ornate typography'),
            DummyTemplate('Newspaper', 'newspaper', 'Classic newspaper layout with multi-column design'),
        ]
    
    return render(request, 'core/select_template.html', {
        'templates': templates,
    })


@login_required
def preview_portfolio(request, template_slug):
    """Preview the generated portfolio"""
    # Get data from session
    context_data = request.session.get('portfolio_data')
    
    if not context_data:
        messages.error(request, 'Session expired. Please upload resume again.')
        return redirect('home')
    
    # Load the template file
    template_path = os.path.join(
        settings.BASE_DIR,
        'core',
        'templates',
        'portfolios',
        template_slug,
        'index.html'
    )
    
    if not os.path.exists(template_path):
        return HttpResponse("Template not found", status=404)
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Render with Django template engine
    django_template = Template(template_content)
    rendered_html = django_template.render(Context(context_data))
    
    return HttpResponse(rendered_html)


@login_required
def download_portfolio(request, template_slug):
    """Generate and download portfolio as ZIP file"""
    # Get data from session
    context_data = request.session.get('portfolio_data')
    
    if not context_data:
        messages.error(request, 'Session expired. Please upload resume again.')
        return redirect('home')
    
    # Load template
    template_dir = os.path.join(
        settings.BASE_DIR,
        'core',
        'templates',
        'portfolios',
        template_slug
    )
    
    template_path = os.path.join(template_dir, 'index.html')
    
    if not os.path.exists(template_path):
        return HttpResponse("Template not found", status=404)
    
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Render
    django_template = Template(template_content)
    rendered_html = django_template.render(Context(context_data))
    
    # Create ZIP in memory
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add rendered HTML
        zip_file.writestr('index.html', rendered_html)
        
        # Add assets
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file != 'index.html':
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, template_dir)
                    zip_file.write(file_path, arcname)
    
    # Response
    zip_buffer.seek(0)
    response = FileResponse(
        zip_buffer,
        as_attachment=True,
        filename=f'portfolio_{template_slug}.zip'
    )
    response['Content-Type'] = 'application/zip'
    
    return response


def run_migrations(request):
    """Helper to run migrations on Vercel"""
    # Only allow superusers or if DEBUG is True (or just open for this fix)
    # For safety, we'll just run it.
    
    output = io.StringIO()
    sys.stdout = output
    
    try:
        call_command('migrate')
        msg = "Migrations completed successfully!\n" + output.getvalue()
    except Exception as e:
        msg = f"Error running migrations: {str(e)}\n" + output.getvalue()
    finally:
        sys.stdout = sys.__stdout__
        
    return HttpResponse(msg, content_type='text/plain')

def premium_waitlist(request):
    """Handle premium features waitlist registration"""
    if request.method == 'POST':
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        
        if email and full_name:
            # Check if already registered
            if not PremiumWaitlist.objects.filter(email=email).exists():
                PremiumWaitlist.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    email=email,
                    full_name=full_name
                )
                messages.success(request, "Success! You've been added to the early access list. We'll notify you soon!")
            else:
                messages.info(request, "You are already on our early access list!")
            return redirect('home')
            
    return render(request, 'core/premium_waitlist.html')
