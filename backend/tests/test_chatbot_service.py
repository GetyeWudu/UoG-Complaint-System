"""
Tests for ChatbotService API key loading
"""
import pytest
from unittest.mock import patch, MagicMock


@pytest.mark.unit
class TestChatbotServiceAPIKeyLoading:
    """Test ChatbotService API key loading with fallback"""
    
    @patch('complaints.chatbot_service.config')
    def test_loads_groq_chatbot_api_key_when_available(self, mock_config):
        """Test that GROQ_CHATBOT_API_KEY is used when available"""
        # Setup mock to return specific key for GROQ_CHATBOT_API_KEY
        def config_side_effect(key, default=''):
            if key == 'GROQ_CHATBOT_API_KEY':
                return 'gsk_chatbot_test_key'
            elif key == 'GROQ_API_KEY':
                return 'gsk_general_test_key'
            elif key == 'GEMINI_API_KEY':
                return ''
            return default
        
        mock_config.side_effect = config_side_effect
        
        # Import after mocking
        from complaints.chatbot_service import ChatbotService
        
        service = ChatbotService()
        
        # Should use the chatbot-specific key
        assert service.groq_api_key == 'gsk_chatbot_test_key'
        assert service.use_groq is True
    
    @patch('complaints.chatbot_service.config')
    def test_falls_back_to_groq_api_key_when_chatbot_key_missing(self, mock_config):
        """Test that GROQ_API_KEY is used as fallback when GROQ_CHATBOT_API_KEY is not set"""
        # Setup mock to return empty for GROQ_CHATBOT_API_KEY but value for GROQ_API_KEY
        def config_side_effect(key, default=''):
            if key == 'GROQ_CHATBOT_API_KEY':
                return default  # Return default (empty)
            elif key == 'GROQ_API_KEY':
                return 'gsk_general_test_key'
            elif key == 'GEMINI_API_KEY':
                return ''
            return default
        
        mock_config.side_effect = config_side_effect
        
        # Import after mocking
        from complaints.chatbot_service import ChatbotService
        
        service = ChatbotService()
        
        # Should use the general GROQ_API_KEY as fallback
        assert service.groq_api_key == 'gsk_general_test_key'
        assert service.use_groq is True
    
    @patch('complaints.chatbot_service.config')
    def test_no_groq_key_when_both_missing(self, mock_config):
        """Test that use_groq is False when both keys are missing"""
        # Setup mock to return empty for both keys
        def config_side_effect(key, default=''):
            return default  # Return default (empty) for all
        
        mock_config.side_effect = config_side_effect
        
        # Import after mocking
        from complaints.chatbot_service import ChatbotService
        
        service = ChatbotService()
        
        # Should have no key
        assert service.groq_api_key == ''
        assert service.use_groq is False
    
    @patch('complaints.chatbot_service.config')
    def test_chatbot_key_takes_precedence_over_general_key(self, mock_config):
        """Test that GROQ_CHATBOT_API_KEY takes precedence when both are available"""
        # Setup mock to return both keys
        def config_side_effect(key, default=''):
            if key == 'GROQ_CHATBOT_API_KEY':
                return 'gsk_chatbot_specific_key'
            elif key == 'GROQ_API_KEY':
                return 'gsk_general_key'
            elif key == 'GEMINI_API_KEY':
                return ''
            return default
        
        mock_config.side_effect = config_side_effect
        
        # Import after mocking
        from complaints.chatbot_service import ChatbotService
        
        service = ChatbotService()
        
        # Should use the chatbot-specific key (takes precedence)
        assert service.groq_api_key == 'gsk_chatbot_specific_key'
        assert service.use_groq is True
