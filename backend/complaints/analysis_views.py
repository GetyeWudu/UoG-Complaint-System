"""
API views for AI complaint analysis
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .complaint_analyzer import complaint_analyzer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_complaint_text(request):
    """
    Analyze complaint text and provide real-time suggestions
    
    POST /api/complaints/analyze/
    Body: {
        "text": "The library is too noisy",
        "category": "Library",
        "language": "en"
    }
    """
    text = request.data.get('text', '').strip()
    category = request.data.get('category')
    language = request.data.get('language', 'en')
    
    if not text:
        return Response(
            {'error': 'Text is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        analysis = complaint_analyzer.analyze_complaint(text, category, language)
        
        return Response({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return Response(
            {'error': f'Analysis failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
