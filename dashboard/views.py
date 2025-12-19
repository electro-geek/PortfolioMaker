from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import Visitor, UserProfile
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard_home(request):
    # User stats
    total_users = User.objects.count()
    users_with_portfolios = UserProfile.objects.filter(has_generated_portfolio=True).count()
    
    # Visitor stats
    total_visits = Visitor.objects.count()
    unique_visitors = Visitor.objects.values('ip_address').distinct().count()
    
    # Recent visits
    recent_visits = Visitor.objects.order_by('-timestamp')[:20]
    
    # Visits by path
    path_stats = Visitor.objects.values('path').annotate(count=Count('id')).order_by('-count')[:10]
    
    # Registered users
    registered_users = User.objects.all().order_by('-date_joined')
    
    context = {
        'total_users': total_users,
        'users_with_portfolios': users_with_portfolios,
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'recent_visits': recent_visits,
        'path_stats': path_stats,
        'registered_users': registered_users,
    }
    
    return render(request, 'dashboard/home.html', context)
