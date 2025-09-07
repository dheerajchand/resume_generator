"""
Admin configuration for user-related models
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import CustomUser, UserProfile, UserResumeData, UserDirectory


class CustomUserAdmin(BaseUserAdmin):
    """Admin interface for CustomUser"""
    
    list_display = ('username', 'email', 'full_name', 'professional_title', 
                   'subscription_tier', 'is_verified', 'resume_count', 'date_joined')
    list_filter = ('subscription_tier', 'is_verified', 'email_verified', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'professional_title')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'website', 'linkedin', 'github', 'location')}),
        ('Professional Info', {'fields': ('professional_title', 'bio')}),
        ('Preferences', {'fields': ('preferred_color_scheme', 'preferred_resume_length')}),
        ('Account Status', {'fields': ('is_verified', 'email_verified', 'subscription_tier')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined', 'last_login_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_joined', 'last_login', 'last_login_at')
    
    def resume_count(self, obj):
        """Display number of resumes created by user"""
        count = obj.resume_count
        if count > 0:
            url = reverse('admin:resumes_resume_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} resumes</a>', url, count)
        return '0 resumes'
    resume_count.short_description = 'Resumes Created'


class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    
    list_display = ('user', 'default_resume_template', 'auto_generate_on_update', 
                   'profile_public', 'created_at')
    list_filter = ('default_resume_template', 'auto_generate_on_update', 
                  'profile_public', 'allow_public_resumes', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Professional Summary', {'fields': ('professional_summary',)}),
        ('Contact Preferences', {'fields': ('show_phone', 'show_email', 'show_website', 'show_linkedin', 'show_github')}),
        ('Resume Preferences', {'fields': ('default_resume_template', 'auto_generate_on_update')}),
        ('Privacy Settings', {'fields': ('profile_public', 'allow_public_resumes')}),
    )


class UserResumeDataAdmin(admin.ModelAdmin):
    """Admin interface for UserResumeData"""
    
    list_display = ('user', 'resume_type', 'length_variant', 'is_active', 
                   'last_generated', 'created_at')
    list_filter = ('resume_type', 'length_variant', 'is_active', 'created_at', 'last_generated')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('Basic Info', {'fields': ('user', 'resume_type', 'length_variant', 'is_active')}),
        ('Content', {'fields': ('personal_info', 'summary', 'competencies', 'experience', 
                               'achievements', 'education', 'projects', 'certifications', 'additional_info')}),
        ('File Management', {'fields': ('input_file_path', 'output_directory', 'last_generated')}),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_generated')
    
    def get_queryset(self, request):
        """Optimize queryset"""
        return super().get_queryset(request).select_related('user')


class UserDirectoryAdmin(admin.ModelAdmin):
    """Admin interface for UserDirectory"""
    
    list_display = ('user', 'is_initialized', 'last_synced', 'created_at')
    list_filter = ('is_initialized', 'created_at', 'last_synced')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    
    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Directories', {'fields': ('input_directory', 'output_directory')}),
        ('Status', {'fields': ('is_initialized', 'last_synced')}),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['initialize_directories']
    
    def initialize_directories(self, request, queryset):
        """Initialize directories for selected users"""
        count = 0
        for directory in queryset:
            try:
                directory.initialize_directories()
                count += 1
            except Exception as e:
                self.message_user(request, f"Error initializing directories for {directory.user.username}: {e}", level='ERROR')
        
        self.message_user(request, f"Successfully initialized directories for {count} users.")
    initialize_directories.short_description = "Initialize directories for selected users"
