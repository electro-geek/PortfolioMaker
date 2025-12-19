import json
import os
from pypdf import PdfReader
import google.generativeai as genai
from django.conf import settings


def extract_text_from_pdf(pdf_file):
    """
    Extract text content from a PDF file
    
    Args:
        pdf_file: Path to the PDF file OR a file-like object
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")


def get_portfolio_data(text, api_key=None):
    """
    Use Google Gemini API to parse resume text and extract structured data
    
    Args:
        text: Raw text extracted from resume PDF
        api_key: Optional user-provided Gemini API key
        
    Returns:
        dict: Structured portfolio data
    """
    try:
        # Configure Gemini API
        api_key_to_use = api_key if api_key else settings.GEMINI_API_KEY
        
        if not api_key_to_use:
            raise Exception("No Gemini API key provided. Please provide one in the premium options.")
            
        # Debug print (masked)
        masked_key = f"{api_key_to_use[:4]}...{api_key_to_use[-4:]}" if len(api_key_to_use) > 8 else "****"
        print(f"DEBUG: Configuring Gemini with key: {masked_key}")
        
        genai.configure(api_key=api_key_to_use)
        
        # Create the model
        model = genai.GenerativeModel('gemini-flash-latest')
        
        # Craft the prompt
        prompt = f"""You are a professional career consultant. Analyze the following resume text and extract structured information.

Resume Text:
{text}

Your task:
1. Extract the following fields: name, title/tagline, bio/about me, experience, projects, skills, contact information (email, phone, linkedin, github, website)
2. If the bio/about me section is missing, synthesize a professional 2-3 sentence summary based on the experience and skills listed
3. If project descriptions are brief, enhance them slightly to be more portfolio-friendly (but stay truthful to the content)
4. For experience and projects, include: title/role, organization/name, duration, description, and technologies/skills used

Return ONLY a valid JSON object with this exact structure:
{{
    "name": "Full Name",
    "tagline": "Professional Title or Tagline",
    "bio": "Professional bio/about me section",
    "contact": {{
        "email": "email@example.com",
        "phone": "+1234567890",
        "linkedin": "linkedin.com/in/username",
        "github": "github.com/username",
        "website": "yourwebsite.com"
    }},
    "skills": ["skill1", "skill2", "skill3"],
    "experience": [
        {{
            "role": "Job Title",
            "company": "Company Name",
            "duration": "Jan 2020 - Present",
            "description": "Brief description of responsibilities and achievements",
            "technologies": ["tech1", "tech2"]
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "duration": "2023",
            "description": "Project description highlighting key features and impact",
            "technologies": ["tech1", "tech2"],
            "link": "github.com/project or demo-link.com"
        }}
    ],
    "education": [
        {{
            "degree": "Degree Name",
            "institution": "University Name",
            "duration": "2015 - 2019",
            "details": "GPA, honors, relevant coursework"
        }}
    ]
}}

Important: Return ONLY the JSON object, no additional text or markdown formatting."""

        # Generate response with retry logic
        import time
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                response = model.generate_content(prompt)
                break
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"Quota exceeded, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise e
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith('```'):
            response_text = response_text.split('```')[1]
            if response_text.startswith('json'):
                response_text = response_text[4:]
        
        # Parse JSON
        portfolio_data = json.loads(response_text.strip())
        
        return portfolio_data
        
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing JSON response from Gemini: {str(e)}\nResponse: {response_text}")
    except Exception as e:
        raise Exception(f"Error getting portfolio data from Gemini: {str(e)}")


def parse_resume_with_gemini(pdf_path):
    """
    Complete pipeline: Extract text from PDF and get structured data from Gemini
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        dict: Structured portfolio data
    """
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        raise Exception("No text could be extracted from the PDF")
    
    # Get structured data from Gemini
    portfolio_data = get_portfolio_data(text)
    
    return portfolio_data
