from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Campus, College, Department, PasswordResetToken, ActivityLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'department', 'campus', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'campus', 'email_verified']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'uog_id']
    
    fieldsets = UserAdmin.fieldsets + (
        ('UoG Information', {
            'fields': ('role', 'uog_id', 'phone_number', 'department', 'campus')
        }),
        ('OAuth', {
            'fields': ('oauth_provider', 'oauth_id', 'oauth_linked_at')
        }),
        ('Security', {
            'fields': ('email_verified', 'last_login_ip', 'failed_login_attempts', 'account_locked_until')
        }),
    )


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    list_display = ['name', 'director']
    search_fields = ['name']


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'campus', 'dean']
    list_filter = ['campus']
    search_fields = ['name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'college', 'head']
    list_filter = ['college__campus']
    search_fields = ['name']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'expires_at', 'used', 'ip_address']
    list_filter = ['used', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['token', 'created_at', 'used_at']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'timestamp', 'ip_address']
    list_filter = ['action', 'timestamp']
    search_fields = ['user__username', 'description']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
