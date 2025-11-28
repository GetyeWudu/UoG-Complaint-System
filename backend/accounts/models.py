from django.contrib.auth.models import AbstractUser
from django.db import models

# 1. Define the Physical & Academic Structure
class Campus(models.Model):
    name = models.CharField(max_length=100) # e.g., "Tewodros", "Maraki"
    director = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='campus_director_of')

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=100) # e.g., "College of Informatics"
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    dean = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='dean_of')

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100) # e.g., "Computer Science"
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    head = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='head_of')

    def __str__(self):
        return f"{self.name} ({self.college.name})"

# 2. Upgrade the User
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('academic', 'Academic Staff'),
        ('non_academic', 'Non-academic Staff'),
        ('proctor', 'Proctor'),
        ('dept_head', 'Department Head'),
        ('dean', 'College Dean'),
        ('maintenance', 'Maintenance Worker'),
        ('admin', 'System Admin'),
        ('super_admin', 'Super Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    
    # Identity Verification
    uog_id = models.CharField(max_length=20, unique=True, null=True, blank=True, help_text="e.g. UGR/1234/12")
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    # Assignments
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    campus = models.ForeignKey(Campus, on_delete=models.SET_NULL, null=True, blank=True)
    
    # OAuth Integration
    oauth_provider = models.CharField(max_length=50, null=True, blank=True, help_text="e.g., 'uog_portal'")
    oauth_id = models.CharField(max_length=255, null=True, blank=True, help_text="OAuth provider user ID")
    oauth_linked_at = models.DateTimeField(null=True, blank=True)
    
    # Two-Factor Authentication
    totp_secret = models.CharField(max_length=32, null=True, blank=True)
    totp_enabled = models.BooleanField(default=False)
    backup_codes = models.JSONField(default=list, blank=True)
    
    # Account Status
    email_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        indexes = [
            models.Index(fields=['oauth_provider', 'oauth_id']),
            models.Index(fields=['uog_id']),
        ]


# Password Reset Token Model
class PasswordResetToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_valid(self):
        from django.utils import timezone
        return not self.used and timezone.now() < self.expires_at
    
    class Meta:
        ordering = ['-created_at']


# Activity Log Model (System-wide audit trail)
class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('login_failed', 'Failed Login Attempt'),
        ('register', 'User Registration'),
        ('password_reset_request', 'Password Reset Requested'),
        ('password_reset_complete', 'Password Reset Completed'),
        ('password_change', 'Password Changed'),
        ('2fa_enabled', '2FA Enabled'),
        ('2fa_disabled', '2FA Disabled'),
        ('oauth_linked', 'OAuth Account Linked'),
        ('complaint_created', 'Complaint Created'),
        ('complaint_updated', 'Complaint Updated'),
        ('complaint_assigned', 'Complaint Assigned'),
        ('complaint_status_changed', 'Complaint Status Changed'),
        ('complaint_closed', 'Complaint Closed'),
        ('file_uploaded', 'File Uploaded'),
        ('file_deleted', 'File Deleted'),
        ('comment_added', 'Comment Added'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('permission_changed', 'Permission Changed'),
        ('settings_changed', 'Settings Changed'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='activity_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional: link to related objects
    related_object_type = models.CharField(max_length=50, null=True, blank=True)
    related_object_id = models.IntegerField(null=True, blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{user_str} - {self.get_action_display()} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
