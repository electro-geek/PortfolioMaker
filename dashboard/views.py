from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import Visitor, UserProfile, PremiumWaitlist
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta

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
    
    # Premium Waitlist
    waitlist_users = PremiumWaitlist.objects.all().order_by('-registered_at')
    total_premium_waitlist = waitlist_users.count()

    context = {
        'total_users': total_users,
        'users_with_portfolios': users_with_portfolios,
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'recent_visits': recent_visits,
        'path_stats': path_stats,
        'registered_users': registered_users,
        'waitlist_users': waitlist_users,
        'total_premium_waitlist': total_premium_waitlist,
    }
    
    return render(request, 'dashboard/home.html', context)
