import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import api from '../api';
import './Chatbot.css';

const Chatbot = () => {
  const { t, i18n } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && messages.length === 0) {
      // Add welcome message
      const welcomeMsg = {
        type: 'bot',
        text: i18n.language === 'am' 
          ? '👋 ሰላም! እኔ የUoG AI ረዳት ነኝ። እንዴት ልረዳዎ እችላለሁ?'
          : '👋 Hello! I\'m the UoG AI Assistant. How can I help you today?',
        timestamp: new Date()
      };
      setMessages([welcomeMsg]);
      loadSuggestions();
    }
  }, [isOpen, i18n.language]);

  const loadSuggestions = async () => {
    try {
      const response = await api.get(`complaints/chatbot/suggestions/?language=${i18n.language}`);
      setSuggestions(response.data.suggestions);
    } catch (error) {
      console.error('Error loading suggestions:', error);
    }
  };

  const sendMessage = async (messageText = null) => {
    const textToSend = messageText || inputMessage.trim();
    if (!textToSend) return;

    // Add user message
    const userMsg = {
      type: 'user',
      text: textToSend,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMsg]);
    setInputMessage('');
    setIsTyping(true);

    try {
      console.log('🤖 Sending message to chatbot:', textToSend);
      console.log('🌐 API URL:', api.defaults.baseURL);
      
      const response = await api.post('complaints/chatbot/message/', {
        message: textToSend,
        language: i18n.language
      });

      console.log('✅ Chatbot response received:', response.data);

      // Simulate typing delay for better UX
      setTimeout(() => {
        const botMsg = {
          type: 'bot',
          text: response.data.response,
          timestamp: new Date(),
          confidence: response.data.confidence,
          topic: response.data.topic
        };
        setMessages(prev => [...prev, botMsg]);
        setIsTyping(false);
      }, 500);

    } catch (error) {
      console.error('❌ Chatbot error:', error);
      console.error('Error details:', error.response?.data);
      console.error('Error status:', error.response?.status);
      
      const errorMsg = {
        type: 'bot',
        text: i18n.language === 'am'
          ? '😔 ይቅርታ፣ ስህተት ተፈጥሯል። እባክዎን እንደገና ይሞክሩ።'
          : '😔 Sorry, something went wrong. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMsg]);
      setIsTyping(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    sendMessage(suggestion);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const clearChat = () => {
    setMessages([]);
    const welcomeMsg = {
      type: 'bot',
      text: i18n.language === 'am' 
        ? '👋 ሰላም! እኔ የUoG AI ረዳት ነኝ። እንዴት ልረዳዎ እችላለሁ?'
        : '👋 Hello! I\'m the UoG AI Assistant. How can I help you today?',
      timestamp: new Date()
    };
    setMessages([welcomeMsg]);
  };

  return (
    <>
      {/* Chat Button */}
      <button 
        className={`chatbot-button ${isOpen ? 'open' : ''}`}
        onClick={toggleChat}
        aria-label="AI Assistant"
      >
        {isOpen ? '✕' : '🤖'}
        {!isOpen && <span className="chatbot-badge">AI</span>}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="chatbot-window">
          {/* Header */}
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <span className="chatbot-avatar">🤖</span>
              <div>
                <h3>{t('chatbot.title', 'AI Assistant')}</h3>
                <span className="chatbot-status">
                  <span className="status-dot"></span>
                  {t('chatbot.online', 'Online')}
                </span>
              </div>
            </div>
            <div className="chatbot-header-actions">
              <button 
                onClick={clearChat} 
                className="chatbot-clear-btn"
                title={t('chatbot.clear', 'Clear chat')}
              >
                🗑️
              </button>
              <button 
                onClick={toggleChat} 
                className="chatbot-close-btn"
                title={t('chatbot.close', 'Close')}
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                <div className="message-content">
                  <div className="message-text">{msg.text}</div>
                  <div className="message-time">
                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="message bot">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Suggestions */}
          {messages.length <= 1 && suggestions.length > 0 && (
            <div className="chatbot-suggestions">
              <p className="suggestions-title">
                {t('chatbot.suggestedQuestions', 'Suggested questions:')}
              </p>
              {suggestions.map((suggestion, index) => (
                <button
                  key={index}
                  className="suggestion-chip"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </button>
              ))}
            </div>
          )}

          {/* Input */}
          <div className="chatbot-input">
            <textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={t('chatbot.placeholder', 'Type your question...')}
              rows="1"
              disabled={isTyping}
            />
            <button 
              onClick={() => sendMessage()}
              disabled={!inputMessage.trim() || isTyping}
              className="send-button"
            >
              ➤
            </button>
          </div>

          {/* Footer */}
          <div className="chatbot-footer">
            <small>
              {t('chatbot.footer', 'Powered by AI • UoG Complaint System')}
            </small>
          </div>
        </div>
      )}
    </>
  );
};

export default Chatbot;
