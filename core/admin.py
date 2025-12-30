from django.contrib import admin
from .models import PortfolioRequest, PortfolioTemplate, PremiumWaitlist, Visitor, UserProfile


@admin.register(PortfolioRequest)
class PortfolioRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'has_extracted_data']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_extracted_data(self, obj):
        return obj.extracted_data is not None
    has_extracted_data.boolean = True
    has_extracted_data.short_description = 'Data Extracted'


@admin.register(PortfolioTemplate)
class PortfolioTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
@admin.register(PremiumWaitlist)
class PremiumWaitlistAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'registered_at', 'user']
    list_filter = ['registered_at']
    search_fields = ['email', 'full_name']
    readonly_fields = ['registered_at']

@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ['ip_address', 'path', 'timestamp', 'session_key']
    list_filter = ['timestamp', 'path']
    search_fields = ['ip_address', 'path']
    readonly_fields = ['timestamp']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_generated_portfolio', 'gemini_api_key_set']
    
    def gemini_api_key_set(self, obj):
        return bool(obj.gemini_api_key)
    gemini_api_key_set.boolean = True
