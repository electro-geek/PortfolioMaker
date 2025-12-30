from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_resume, name='upload_resume'),
    path('select-template/', views.select_template, name='select_template'),
    path('preview/<slug:template_slug>/', views.preview_portfolio, name='preview_portfolio'),
    path('download/<slug:template_slug>/', views.download_portfolio, name='download_portfolio'),
    path('api/login/', views.firebase_login, name='firebase_login'),
    path('run-migrations/', views.run_migrations, name='run_migrations'),
    path('logout/', views.logout_view, name='logout'),
    path('clear-api-key/', views.clear_api_key, name='clear_api_key'),
    path('premium-waitlist/', views.premium_waitlist, name='premium_waitlist'),
]
