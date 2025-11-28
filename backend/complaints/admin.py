from django.contrib import admin
from .models import (
    Category, SubCategory, Complaint, ComplaintEvent, ComplaintComment,
    ComplaintFile, RoutingRule, EmailTemplate
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['tracking_id', 'title', 'status', 'priority', 'submitter', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'campus', 'category', 'is_anonymous', 'created_at']
    search_fields = ['tracking_id', 'title', 'description', 'submitter__username']
    readonly_fields = ['tracking_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tracking_id', 'title', 'description', 'submitter', 'is_anonymous', 'anonymous_email')
        }),
        ('Categorization', {
            'fields': ('category', 'sub_category', 'campus', 'department', 'location')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'urgency', 'assigned_to')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'assigned_at', 'resolved_at', 'closed_at')
        }),
        ('Resolution', {
            'fields': ('resolution_notes', 'rejection_reason')
        }),
        ('Feedback', {
            'fields': ('feedback_rating', 'feedback_comment', 'feedback_submitted_at')
        }),
    )


@admin.register(ComplaintEvent)
class ComplaintEventAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'event_type', 'actor', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['complaint__tracking_id', 'notes']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(ComplaintComment)
class ComplaintCommentAdmin(admin.ModelAdmin):
    list_display = ['complaint', 'author', 'created_at', 'is_internal']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['complaint__tracking_id', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ComplaintFile)
class ComplaintFileAdmin(admin.ModelAdmin):
    list_display = ['filename', 'complaint', 'uploaded_by', 'file_size', 'uploaded_at']
    list_filter = ['mime_type', 'uploaded_at']
    search_fields = ['filename', 'complaint__tracking_id']
    readonly_fields = ['uploaded_at', 'file_size']


@admin.register(RoutingRule)
class RoutingRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'campus', 'assign_to_department', 'priority', 'is_active']
    list_filter = ['is_active', 'category', 'campus']
    search_fields = ['name', 'description']


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'updated_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'subject']
    readonly_fields = ['created_at', 'updated_at']
