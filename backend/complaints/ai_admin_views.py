"""
Admin views for AI validation management
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .ai_validator import validate_complaint, check_duplicate
from .models import Complaint
from django.utils import timezone


class ValidateComplaintView(APIView):
    """
    Admin endpoint to validate a complaint using AI
    POST /api/complaints/validate/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        title = request.data.get('title', '')
        description = request.data.get('description', '')
        
        if not title or not description:
            return Response(
                {'error': 'Title and description are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Run AI validation
        validation_result = validate_complaint(title, description)
        
        # Check for duplicates if user is authenticated
        duplicate_result = {'is_duplicate': False, 'similar_complaints': []}
        if request.user.is_authenticated:
            recent_complaints = Complaint.objects.filter(
                submitter=request.user,
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).values('id', 'tracking_id', 'title', 'description')
            
            duplicate_result = check_duplicate(title, description, list(recent_complaints))
        
        return Response({
            'validation': validation_result,
            'duplicate_check': duplicate_result
        })


class ComplaintStatsView(APIView):
    """
    Get AI validation statistics
    GET /api/complaints/ai-stats/
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Only admins can view stats
        if request.user.role not in ['admin', 'super_admin']:
            return Response(
                {'error': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get recent complaints for analysis
        recent_complaints = Complaint.objects.filter(
            created_at__gte=timezone.now() - timezone.timedelta(days=30)
        )
        
        total_complaints = recent_complaints.count()
        
        # Analyze each complaint
        valid_count = 0
        spam_count = 0
        unclear_count = 0
        
        for complaint in recent_complaints[:100]:  # Limit to 100 for performance
            result = validate_complaint(complaint.title, complaint.description)
            if result['is_valid']:
                valid_count += 1
            if 'potential_spam' in result['flags']:
                spam_count += 1
            if 'unclear_complaint' in result['flags']:
                unclear_count += 1
        
        return Response({
            'total_complaints': total_complaints,
            'analyzed': min(100, total_complaints),
            'valid_percentage': (valid_count / min(100, total_complaints) * 100) if total_complaints > 0 else 0,
            'spam_detected': spam_count,
            'unclear_complaints': unclear_count,
            'period': '30 days'
        })
