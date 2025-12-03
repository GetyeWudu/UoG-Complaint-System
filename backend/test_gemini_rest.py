"""
Quick test script for Gemini REST API
"""
import sys
import os

# Add the project to path
sys.path.insert(0, os.path.dirname(__file__))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

# Now test the chatbot
from complaints.chatbot_service import chatbot_service

print("=" * 60)
print("🧪 TESTING GEMINI REST API CHATBOT")
print("=" * 60)

# Test question
test_question = "What are the library hours?"
print(f"\n📝 Question: {test_question}")

try:
    response = chatbot_service.get_response(test_question, language='en')
    print(f"\n✅ Response received!")
    print(f"📊 Source: {response['source']}")
    print(f"🎯 Confidence: {response['confidence']}")
    print(f"\n💬 Answer:\n{response['response']}")
    print("\n" + "=" * 60)
    print("✅ SUCCESS! Gemini REST API is working!")
    print("=" * 60)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
