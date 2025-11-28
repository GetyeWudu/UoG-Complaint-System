from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


# Category and SubCategory Models
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    class Meta:
        verbose_name_plural = 'SubCategories'
        unique_together = ['category', 'name']
        ordering = ['category', 'name']


class Complaint(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
    ]
    
    # Basic Information
    tracking_id = models.CharField(max_length=50, unique=True, default=uuid.uuid4, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    # Categorization
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='complaints')
    
    # Location
    campus = models.ForeignKey('accounts.Campus', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255, help_text="Specific location detail")
    
    # Status & Priority
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new', db_index=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    urgency = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='low')  # AI-determined
    
    # People
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submitted_complaints', 
                                   on_delete=models.SET_NULL, null=True, blank=True,
                                   help_text="Null for anonymous complaints")
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_complaints', 
                                     on_delete=models.SET_NULL, null=True, blank=True)
    
    # Anonymous submission support
    is_anonymous = models.BooleanField(default=False)
    anonymous_email = models.EmailField(null=True, blank=True, help_text="Optional email for anonymous submitter")
    
    # Legacy fields (for backward compatibility)
    is_academic = models.BooleanField(default=False)
    is_facility = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_at = models.DateTimeField(null=True, blank=True)
    in_progress_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Feedback System
    feedback_rating = models.IntegerField(null=True, blank=True, help_text="1 to 5 stars")
    feedback_comment = models.TextField(blank=True)
    feedback_submitted_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolution_notes = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tracking_id} - {self.title}"
    
    def time_to_resolution(self):
        """Calculate time from creation to resolution in hours"""
        if self.resolved_at:
            delta = self.resolved_at - self.created_at
            return delta.total_seconds() / 3600
        return None
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['campus', 'status']),
        ]



# Complaint Event Model (Audit Trail)
class ComplaintEvent(models.Model):
    EVENT_TYPES = [
        ('created', 'Created'),
        ('assigned', 'Assigned'),
        ('status_changed', 'Status Changed'),
        ('priority_changed', 'Priority Changed'),
        ('comment_added', 'Comment Added'),
        ('file_attached', 'File Attached'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('rejected', 'Rejected'),
        ('reopened', 'Reopened'),
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=30, choices=EVENT_TYPES)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Event details
    old_value = models.CharField(max_length=255, blank=True)
    new_value = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    # Metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        actor_str = self.actor.username if self.actor else 'System'
        return f"{self.complaint.tracking_id} - {self.get_event_type_display()} by {actor_str}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['complaint', '-timestamp']),
        ]


# Complaint Comment Model (Threaded Messaging)
class ComplaintComment(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Visibility
    is_internal = models.BooleanField(default=False, help_text="Internal notes not visible to submitter")
    
    def __str__(self):
        return f"Comment by {self.author.username if self.author else 'Unknown'} on {self.complaint.tracking_id}"
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['complaint', 'created_at']),
        ]


# Complaint File Model (Multiple Attachments)
class ComplaintFile(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='files')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    file = models.FileField(upload_to='complaints/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    mime_type = models.CharField(max_length=100)
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Optional: link to comment
    comment = models.ForeignKey(ComplaintComment, on_delete=models.SET_NULL, null=True, blank=True, related_name='attachments')
    
    def __str__(self):
        return f"{self.filename} - {self.complaint.tracking_id}"
    
    class Meta:
        ordering = ['-uploaded_at']


# Routing Rule Model (Auto-assignment Configuration)
class RoutingRule(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher priority rules are evaluated first")
    
    # Conditions
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    campus = models.ForeignKey('accounts.Campus', on_delete=models.CASCADE, null=True, blank=True)
    
    # Actions
    assign_to_department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True)
    assign_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    set_priority = models.CharField(max_length=10, choices=Complaint.PRIORITY_CHOICES, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-priority', 'name']


# Email Template Model
class EmailTemplate(models.Model):
    TEMPLATE_TYPES = [
        ('submission_confirmation', 'Submission Confirmation'),
        ('assignment_notification', 'Assignment Notification'),
        ('status_change', 'Status Change Notification'),
        ('resolution_notification', 'Resolution Notification'),
        ('password_reset', 'Password Reset'),
        ('welcome', 'Welcome Email'),
        ('2fa_code', '2FA Code'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=255)
    
    # Email content
    html_content = models.TextField(help_text="HTML version of email")
    text_content = models.TextField(help_text="Plain text version of email")
    
    # Template variables documentation
    available_variables = models.TextField(blank=True, help_text="JSON list of available template variables")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"
    
    class Meta:
        ordering = ['template_type', 'name']
