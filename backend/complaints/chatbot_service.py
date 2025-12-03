"""
SUPER POWERFUL AI Chatbot Service for UoG
Powered by Google Gemini AI (FREE!) - Using REST API
"""
import os
import json
import re
import requests
from typing import Dict, List, Optional
from django.conf import settings
from decouple import config

class ChatbotService:
    """The most powerful AI chatbot for university support - Powered by Google Gemini REST API"""
    
    def __init__(self):
        # Try Groq first (faster and more generous limits!)
        self.groq_api_key = config('GROQ_API_KEY', default='')
        self.use_groq = bool(self.groq_api_key)
        
        # Fallback to Gemini
        self.gemini_api_key = config('GEMINI_API_KEY', default='')
        self.use_gemini = bool(self.gemini_api_key) and not self.use_groq
        
        print(f"🔍 Groq API Key loaded: {'Yes' if self.groq_api_key else 'No'}")
        print(f"🔍 Gemini API Key loaded: {'Yes' if self.gemini_api_key else 'No'}")
        
        # Initialize Groq if available (PREFERRED - faster and better limits!)
        if self.use_groq:
            try:
                # Using REST API - no package needed!
                print("✅ Groq AI initialized successfully! (FAST & FREE - REST API)")
            except Exception as e:
                print(f"⚠️ Groq initialization failed: {e}")
                self.use_groq = False
                self.use_gemini = bool(self.gemini_api_key)
        
        # Initialize Gemini REST API if available (fallback)
        if self.use_gemini and not self.use_groq:
            try:
                # Use the v1beta API with gemini-2.5-flash (free and fast model)
                self.gemini_api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.gemini_api_key}"
                print("✅ Google Gemini AI initialized successfully (REST API)!")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
                self.use_gemini = False
        
        # Load comprehensive UoG knowledge base
        try:
            from .uog_knowledge_base import UOG_KNOWLEDGE
            base_knowledge = UOG_KNOWLEDGE.copy()
        except Exception as e:
            print(f"Warning: Could not load UOG_KNOWLEDGE: {e}")
            base_knowledge = {}
        
        # Use the comprehensive UoG knowledge base
        self.knowledge_base = base_knowledge
        
        # Build context for Gemini from knowledge base
        self.uog_context = self._build_uog_context()
    
    def _build_uog_context(self) -> str:
        """Build comprehensive UoG context for Gemini"""
        context_parts = []
        
        for topic, data in self.knowledge_base.items():
            response = data.get('response_en', '')
            if response:
                context_parts.append(f"Topic: {topic}\n{response}\n")
        
        return "\n".join(context_parts)
    
    def get_response(self, message: str, language: str = 'en') -> Dict:
        """
        Get chatbot response - POWERED BY GOOGLE GEMINI AI!
        
        Args:
            message: User's message
            language: 'en' or 'am'
            
        Returns:
            Dict with response and metadata
        """
        try:
            message_lower = message.lower().strip()
            
            if not message_lower:
                return self._get_default_response(language)
            
            # Use Groq AI if available (FASTEST & BEST!)
            if self.use_groq:
                try:
                    return self._get_groq_response(message, language)
                except Exception as e:
                    print(f"Groq error: {e}")
                    # Fall through to Gemini or keyword matching
            
            # Use Gemini AI if available (fallback)
            if self.use_gemini:
                try:
                    return self._get_gemini_response(message, language)
                except Exception as e:
                    print(f"Gemini error: {e}")
                    # Fall through to keyword matching
            
            # Fallback: Check knowledge base (rule-based)
            best_match = None
            best_score = 0
            
            for topic, data in self.knowledge_base.items():
                matches = sum(1 for keyword in data.get('keywords', []) if keyword in message_lower)
                if matches > best_score:
                    best_score = matches
                    best_match = (topic, data)
            
            if best_match and best_score > 0:
                topic, data = best_match
                response_key = f'response_{language}'
                return {
                    'response': data.get(response_key, data.get('response_en', 'Information not available')),
                    'source': 'knowledge_base',
                    'topic': topic,
                    'confidence': min(0.9, 0.5 + (best_score * 0.1))
                }
            
            # Default helpful response
            return self._get_default_response(language)
            
        except Exception as e:
            print(f"Chatbot error: {e}")
            return self._get_error_response(language)
    
    def _get_groq_response(self, message: str, language: str) -> Dict:
        """Get intelligent response from Groq AI using REST API (FAST & FREE!)"""
        try:
            # Build prompt with UoG context
            system_prompt = f"""You are an intelligent AI assistant for University of Gondar (UoG) in Ethiopia.

Your role is to help students, staff, and visitors with accurate information about the university.

Here is comprehensive information about UoG:

{self.uog_context}

IMPORTANT INSTRUCTIONS:
1. Answer questions accurately based on the information provided above
2. Be conversational and natural (like ChatGPT)
3. If asked about specific colleges, departments, or programs, provide detailed information
4. Always include relevant contact information (phone numbers, emails, websites)
5. If you don't know something, direct them to the appropriate office (usually Registrar)
6. Be helpful, friendly, and professional
7. Keep responses concise but informative
8. Do NOT use markdown formatting like **bold** - use plain natural text
9. Use bullet points with - instead of special characters"""

            if language == 'am':
                system_prompt += "\n10. Respond in Amharic language."
            else:
                system_prompt += "\n10. Respond in English language."
            
            # Call Groq REST API
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            # Debug: Check API key
            print(f"🔑 Using Groq API key: {self.groq_api_key[:20]}...")
            
            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            response_text = data['choices'][0]['message']['content']
            
            print(f"✅ Groq AI responded successfully!")
            
            return {
                'response': response_text,
                'source': 'groq_ai',
                'topic': 'ai_generated',
                'confidence': 0.95
            }
            
        except Exception as e:
            print(f"Groq API error: {e}")
            raise e
    
    def _get_gemini_response(self, message: str, language: str) -> Dict:
        """Get intelligent response from Google Gemini AI using REST API with retry logic"""
        import time
        
        max_retries = 3
        base_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                # Build prompt with UoG context
                system_prompt = f"""You are an intelligent AI assistant for University of Gondar (UoG) in Ethiopia.

Your role is to help students, staff, and visitors with accurate information about the university.

Here is comprehensive information about UoG:

{self.uog_context}

IMPORTANT INSTRUCTIONS:
1. Answer questions accurately based on the information provided above
2. Be conversational and natural (like ChatGPT)
3. If asked about specific colleges, departments, or programs, provide detailed information
4. Always include relevant contact information (phone numbers, emails, websites)
5. If you don't know something, direct them to the appropriate office (usually Registrar)
6. Be helpful, friendly, and professional
7. Keep responses concise but informative
8. Do NOT use markdown formatting like **bold** - use plain natural text
9. Use bullet points with - instead of special characters"""

                if language == 'am':
                    system_prompt += "\n10. Respond in Amharic language."
                else:
                    system_prompt += "\n10. Respond in English language."
                
                # Create the full prompt
                full_prompt = f"{system_prompt}\n\nUser Question: {message}\n\nYour Response:"
                
                # Create the request payload for Gemini REST API
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": full_prompt
                        }]
                    }],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 1024,
                    }
                }
                
                headers = {
                    'Content-Type': 'application/json'
                }
                
                # Make the API request
                response = requests.post(
                    self.gemini_api_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )
                
                # Check for rate limiting
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt)  # Exponential backoff
                        print(f"⏳ Rate limited. Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"❌ Rate limit exceeded after {max_retries} attempts. Using knowledge base.")
                        raise Exception("Rate limit exceeded")
                
                response.raise_for_status()
                
                # Parse the response
                data = response.json()
                
                # Extract the response text
                if 'candidates' in data and len(data['candidates']) > 0:
                    candidate = data['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        response_text = candidate['content']['parts'][0]['text']
                        print(f"✅ Gemini AI responded successfully!")
                        return {
                            'response': response_text,
                            'source': 'gemini_rest_api',
                            'topic': 'ai_generated',
                            'confidence': 0.95
                        }
                
                raise Exception("No valid response from Gemini API")
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    continue
                print(f"Gemini REST API error: {e}")
                raise e
            except Exception as e:
                print(f"Gemini REST API error: {e}")
                raise e
        
        raise Exception("Failed after all retries")
    
    def _get_default_response(self, language: str) -> Dict:
        """Get default helpful response"""
        if language == 'am':
            return {
                'response': """ይቅርታ፣ ያንን ጥያቄ ሙሉ በሙሉ አልገባኝም። እባክዎን ይበልጥ ግልጽ ሊሆኑ ይችላሉ?

የሚከተሉትን ጥያቄዎች መሞከር ይችላሉ:

🎓 **ስለ ዩኒቨርሲቲ:** "ስለ UoG ንገረኝ"
📚 **ቤተ-መጽሐፍት:** "የቤተ-መጽሐፍት ሰዓት ምንድን ነው?"
📝 **ምዝገባ:** "እንዴት ኮርስ መመዝገብ እችላለሁ?"
📶 **WiFi:** "WiFi የይለፍ ቃል እንዴት አገኛለሁ?"
🍽️ **ካፌቴሪያ:** "የካፌቴሪያ ሰዓት ምንድን ነው?"
📋 **ፈተናዎች:** "የፈተና መርሃግብር መቼ ይለጠፋል?"
💰 **ክፍያዎች:** "ክፍያው ምን ያህል ነው?"
🏛️ **ኮሌጆች:** "ምን ፕሮግራሞች አሉ?"

ወይም በራስዎ ቃላት ይጠይቁ!""",
                'source': 'default',
                'topic': 'help',
                'confidence': 0.5
            }
        else:
            return {
                'response': """I'm not sure I fully understand that question. Could you be more specific?

Here are some questions you can ask me:

🎓 **About University:** "Tell me about UoG"
📚 **Library:** "What are library hours?"
📝 **Registration:** "How do I register for courses?"
📶 **WiFi:** "How do I get WiFi password?"
🍽️ **Cafeteria:** "What are cafeteria hours?"
📋 **Exams:** "When are exams?"
💰 **Fees:** "How much is tuition?"
🏛️ **Colleges:** "What programs are available?"
🎯 **Admission:** "How do I apply?"

Or ask in your own words - I'm here to help!""",
                'source': 'default',
                'topic': 'help',
                'confidence': 0.5
            }
    
    def _get_error_response(self, language: str) -> Dict:
        """Get error response"""
        if language == 'am':
            return {
                'response': "😔 ይቅርታ፣ ስህተት ተፈጥሯል። እባክዎን እንደገና ይሞክሩ።",
                'source': 'error',
                'topic': 'error',
                'confidence': 0.0
            }
        else:
            return {
                'response': "😔 Sorry, something went wrong. Please try again.",
                'source': 'error',
                'topic': 'error',
                'confidence': 0.0
            }
    

    
    def get_suggested_questions(self, language: str = 'en') -> List[str]:
        """Get suggested questions for users"""
        if language == 'am':
            return [
                "የቤተ-መጽሐፍት ሰዓት ምንድን ነው?",
                "እንዴት ኮርስ መመዝገብ እችላለሁ?",
                "WiFi የይለፍ ቃል እንዴት አገኛለሁ?",
                "የካፌቴሪያ ሰዓት ምንድን ነው?",
                "የፈተና መርሃግብር መቼ ይለጠፋል?"
            ]
        else:
            return [
                "What are the library hours?",
                "How do I register for courses?",
                "How do I get WiFi password?",
                "What are cafeteria hours?",
                "When is the exam schedule posted?"
            ]


# Singleton instance
chatbot_service = ChatbotService()
