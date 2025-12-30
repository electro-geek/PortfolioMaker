from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_generated_portfolio = models.BooleanField(default=False)
    gemini_api_key = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class PortfolioTemplate(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PortfolioRequest(models.Model):
    # Optional: link to user if you want to track who made the request
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    resume_file = models.FileField(upload_to='resumes/', null=True, blank=True)
    extracted_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request {self.id} at {self.created_at}"

class Visitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return f"Visit from {self.ip_address} to {self.path} at {self.timestamp}"

class PremiumWaitlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.email} - {self.registered_at.strftime('%Y-%m-%d')}"

# Signal to automatically create/save UserProfile when User is created/saved
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
