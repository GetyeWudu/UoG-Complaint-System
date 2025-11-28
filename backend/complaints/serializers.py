from rest_framework import serializers
from .models import Complaint, Category, SubCategory, ComplaintFile, ComplaintComment, ComplaintEvent
from django.contrib.auth import get_user_model
from .validators import validate_file_size, validate_file_extension

User = get_user_model()


class ComplaintFileSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintFile
        fields = ['id', 'file', 'file_url', 'filename', 'file_size', 'mime_type', 
                  'uploaded_by', 'uploaded_by_username', 'uploaded_at']
        read_only_fields = ['id', 'filename', 'file_size', 'mime_type', 'uploaded_by', 'uploaded_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if request and obj.file:
            return request.build_absolute_uri(f'/api/complaints/files/{obj.id}/download/')
        return None
    
    def validate_file(self, value):
        validate_file_size(value)
        validate_file_extension(value)
        return value


class ComplaintCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintComment
        fields = ['id', 'complaint', 'author', 'author_username', 'author_name', 
                  'parent', 'content', 'is_internal', 'created_at', 'updated_at', 'replies']
        read_only_fields = ['id', 'complaint', 'author', 'parent', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        if obj.author:
            return obj.author.get_full_name() or obj.author.username
        return 'Unknown'
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return ComplaintCommentSerializer(obj.replies.all(), many=True, context=self.context).data
        return []


class ComplaintEventSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = ComplaintEvent
        fields = ['id', 'complaint', 'event_type', 'event_type_display', 'actor', 
                  'actor_username', 'timestamp', 'old_value', 'new_value', 'notes', 'metadata']
        read_only_fields = ['id', 'timestamp']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active']


class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'description', 'category', 'category_name', 'is_active']

class ComplaintSerializer(serializers.ModelSerializer):
    submitter_username = serializers.CharField(source='submitter.username', read_only=True)
    submitter_name = serializers.SerializerMethodField()
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to_name = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    campus_name = serializers.CharField(source='campus.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    # Related data
    files = ComplaintFileSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    
    # File uploads (write-only)
    uploaded_files = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'tracking_id', 'title', 'description', 
            'category', 'category_name', 'sub_category', 'sub_category_name',
            'campus', 'campus_name', 'department', 'department_name', 'location',
            'status', 'priority', 'urgency',
            'submitter', 'submitter_username', 'submitter_name',
            'assigned_to', 'assigned_to_username', 'assigned_to_name',
            'is_anonymous', 'anonymous_email',
            'is_academic', 'is_facility',
            'created_at', 'updated_at', 'assigned_at', 'resolved_at', 'closed_at',
            'feedback_rating', 'feedback_comment', 'feedback_submitted_at',
            'resolution_notes', 'rejection_reason',
            'files', 'comments', 'events', 'uploaded_files'
        ]
        read_only_fields = [
            'id', 'tracking_id', 'urgency', 'created_at', 'updated_at',
            'assigned_at', 'resolved_at', 'closed_at', 'feedback_submitted_at'
        ]
    
    def get_submitter_name(self, obj):
        if obj.is_anonymous:
            return 'Anonymous'
        if obj.submitter:
            return obj.submitter.get_full_name() or obj.submitter.username
        return 'Unknown'
    
    def get_assigned_to_name(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.get_full_name() or obj.assigned_to.username
        return None
    
    def get_comments(self, obj):
        # Only return top-level comments (replies are nested)
        comments = obj.comments.filter(parent__isnull=True)
        return ComplaintCommentSerializer(comments, many=True, context=self.context).data
    
    def get_events(self, obj):
        # Return recent events (last 10)
        events = obj.events.all()[:10]
        return ComplaintEventSerializer(events, many=True).data
    
    def create(self, validated_data):
        # Remove uploaded_files from validated_data as it's handled in the view
        validated_data.pop('uploaded_files', None)
        return super().create(validated_data)