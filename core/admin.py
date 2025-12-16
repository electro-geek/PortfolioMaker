from django.contrib import admin
from .models import PortfolioRequest, PortfolioTemplate


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
    readonly_fields = ['created_at']
