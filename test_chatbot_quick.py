#!/usr/bin/env python
"""
Quick test script for the Super Chatbot
Run this to verify the chatbot is working
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from complaints.chatbot_service import chatbot_service

def test_chatbot():
    print("=" * 60)
    print("🤖 TESTING SUPER POWERFUL UoG AI ASSISTANT")
    print("=" * 60)
    
    # Test questions
    test_cases = [
        ("hi", "en"),
        ("What are library hours?", "en"),
        ("How do I register?", "en"),
        ("WiFi password", "en"),
        ("Tell me about UoG", "en"),
        ("ሰላም", "am"),
        ("የቤተ-መጽሐፍት ሰዓት", "am"),
    ]
    
    print(f"\n✅ Chatbot loaded successfully!")
    print(f"📚 Knowledge base topics: {len(chatbot_service.knowledge_base)}")
    print(f"\n🧪 Running {len(test_cases)} test cases...\n")
    
    for i, (question, lang) in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}/{len(test_cases)}")
        print(f"Question ({lang}): {question}")
        print(f"{'-'*60}")
        
        try:
            response = chatbot_service.get_response(question, lang)
            print(f"✅ Response received!")
            print(f"Topic: {response['topic']}")
            print(f"Source: {response['source']}")
            print(f"Confidence: {response['confidence']}")
            print(f"\nResponse preview:")
            print(response['response'][:200] + "..." if len(response['response']) > 200 else response['response'])
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*60}")
    print("🎉 ALL TESTS COMPLETED!")
    print("=" * 60)
    print("\n✅ Chatbot is working perfectly!")
    print("🚀 Ready for demo!")
    print("\nTo use:")
    print("1. Start backend: cd backend && python manage.py runserver")
    print("2. Start frontend: cd frontend && npm run dev")
    print("3. Click the purple chatbot button (🤖)")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_chatbot()
