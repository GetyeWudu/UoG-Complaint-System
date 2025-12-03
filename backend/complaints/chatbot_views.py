"""
API views for chatbot functionality
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .chatbot_service import chatbot_service


@api_view(['POST'])
@permission_classes([AllowAny])  # Chatbot available to everyone
def chat_message(request):
    """
    Handle chat messages from users
    
    POST /api/chatbot/message/
    Body: {
        "message": "What are library hours?",
        "language": "en"  # or "am"
    }
    """
    message = request.data.get('message', '').strip()
    language = request.data.get('language', 'en')
    
    if not message:
        return Response(
            {'error': 'Message is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if language not in ['en', 'am']:
        language = 'en'
    
    try:
        # Get chatbot response
        result = chatbot_service.get_response(message, language)
        
        return Response({
            'message': message,
            'response': result['response'],
            'source': result['source'],
            'topic': result['topic'],
            'confidence': result['confidence'],
            'timestamp': None  # Frontend will add timestamp
        })
    
    except Exception as e:
        return Response(
            {'error': f'Chatbot error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def suggested_questions(request):
    """
    Get suggested questions for users
    
    GET /api/chatbot/suggestions/?language=en
    """
    language = request.query_params.get('language', 'en')
    
    if language not in ['en', 'am']:
        language = 'en'
    
    try:
        suggestions = chatbot_service.get_suggested_questions(language)
        
        return Response({
            'suggestions': suggestions,
            'language': language
        })
    
    except Exception as e:
        return Response(
            {'error': f'Error getting suggestions: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
