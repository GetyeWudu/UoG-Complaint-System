"""
Simple test for Gemini REST API (no Django needed)
"""
import requests
import json
from decouple import config

# Get API key
GEMINI_API_KEY = config('GEMINI_API_KEY', default='')

if not GEMINI_API_KEY:
    print("❌ No GEMINI_API_KEY found in .env")
    exit(1)

print(f"✅ API Key loaded: {GEMINI_API_KEY[:10]}...")

# First, list available models
print("\n📋 Listing available models...")
list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"

try:
    response = requests.get(list_url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        print("\n✅ Available models:")
        for model in data.get('models', []):
            name = model.get('name', '')
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"  - {name}")
    else:
        print(f"❌ Could not list models: {response.status_code}")
except Exception as e:
    print(f"❌ Error listing models: {e}")

# Try with gemini-2.5-flash (free and fast model)
print("\n" + "="*60)
print("🧪 Testing with gemini-2.5-flash model...")
print("="*60)

api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

# Create test payload
payload = {
    "contents": [{
        "parts": [{
            "text": "Hello! Can you tell me about University of Gondar in one sentence?"
        }]
    }]
}

print("\n📤 Sending request to Gemini...")

try:
    response = requests.post(
        api_url,
        json=payload,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )
    
    print(f"📥 Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if 'candidates' in data and len(data['candidates']) > 0:
            text = data['candidates'][0]['content']['parts'][0]['text']
            print(f"\n✅ SUCCESS! Gemini responded:\n{text}")
            print("\n" + "="*60)
            print("🎉 GEMINI REST API IS WORKING!")
            print("="*60)
        else:
            print(f"❌ Unexpected response format: {json.dumps(data, indent=2)}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
