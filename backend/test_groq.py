"""
Test Groq API directly
"""
from decouple import config

print("Testing Groq import...")

try:
    from groq import Groq
    print("✅ Groq module imported successfully!")
    
    # Get API key
    api_key = config('GROQ_API_KEY', default='')
    print(f"✅ API Key loaded: {api_key[:20]}...")
    
    # Initialize client
    client = Groq(api_key=api_key)
    print("✅ Groq client initialized!")
    
    # Test API call
    print("\n🧪 Testing API call...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Say 'Hello from Groq!' in one sentence.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response = chat_completion.choices[0].message.content
    print(f"\n✅ SUCCESS! Groq responded:\n{response}")
    print("\n" + "="*60)
    print("🎉 GROQ IS WORKING PERFECTLY!")
    print("="*60)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("\nTry: pip install groq")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
