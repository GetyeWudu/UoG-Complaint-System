"""
Test Groq REST API directly
"""
import requests
from decouple import config

# Get API key
api_key = config('GROQ_API_KEY', default='')
print(f"✅ API Key: {api_key[:20]}...")

# Test API call
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {
            "role": "user",
            "content": "Say 'Hello from Groq!' in one sentence."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

print("\n📤 Sending request to Groq...")

try:
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"📥 Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        text = data['choices'][0]['message']['content']
        print(f"\n✅ SUCCESS! Groq responded:\n{text}")
        print("\n" + "="*60)
        print("🎉 GROQ REST API IS WORKING!")
        print("="*60)
    else:
        print(f"❌ Error: {response.text}")
        
except Exception as e:
    print(f"❌ Exception: {e}")
    import traceback
    traceback.print_exc()
