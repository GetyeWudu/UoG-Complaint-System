"""
AI-powered complaint analysis service
Provides real-time feedback and suggestions for complaint drafting
"""
import requests
from decouple import config


class ComplaintAnalyzer:
    def __init__(self):
        # Use dedicated API key for AI analysis to maximize rate limits
        self.api_key = config('GROQ_API_KEY')  # Dedicated for AI analysis
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"
    
    def analyze_complaint(self, text, category=None, language='en'):
        """
        Analyze complaint text and provide suggestions
        
        Returns:
        {
            'completeness_score': 0-100,
            'clarity_score': 0-100,
            'missing_info': ['location', 'date', 'evidence'],
            'suggestions': ['Add specific location', 'Include date and time'],
            'tone': 'professional' | 'angry' | 'neutral',
            'detected_category': 'Academic' | 'Facility' | etc,
            'urgency': 'low' | 'medium' | 'high' | 'critical'
        }
        """
        if not text or len(text.strip()) < 10:
            return {
                'completeness_score': 0,
                'clarity_score': 0,
                'missing_info': ['description', 'location', 'date', 'evidence'],
                'suggestions': ['Start by describing your issue clearly'],
                'tone': 'neutral',
                'detected_category': None,
                'urgency': 'low'
            }
        
        prompt = self._build_analysis_prompt(text, category, language)
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                    "max_tokens": 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                return self._parse_ai_response(ai_response)
            else:
                return self._get_fallback_analysis(text)
                
        except Exception as e:
            print(f"AI Analysis error: {e}")
            return self._get_fallback_analysis(text)
    
    def _build_analysis_prompt(self, text, category, language):
        """Build the prompt for AI analysis"""
        
        # Amharic-specific prompt
        if language == 'am':
            return f"""የዚህን የአማርኛ ቅሬታ ጽሑፍ ተንትን እና በJSON ቅርጸት መልስ ስጥ።

የቅሬታ ጽሑፍ: "{text}"
ምድብ: {category or 'ያልታወቀ'}

ይህን ትክክለኛ JSON መዋቅር ብቻ መልስ:
{{
    "completeness_score": <0-100 ቁጥር>,
    "clarity_score": <0-100 ቁጥር>,
    "missing_info": ["ቦታ", "ቀን", "ማስረጃ", "ተጽእኖ"],
    "suggestions": ["ተግባራዊ ምክር 1", "ተግባራዊ ምክር 2", "ተግባራዊ ምክር 3"],
    "tone": "professional",
    "detected_category": "Academic",
    "urgency": "medium"
}}

የግምገማ መስፈርቶች:
- ሙሉነት (completeness): ምን፣ የት፣ መቼ፣ ማን፣ ማስረጃ ያካትታል?
- ግልጽነት (clarity): ልዩ እና ለመረዳት ቀላል ነው?
- ቃና (tone): "professional", "angry", "frustrated", "neutral" ውስጥ አንዱ
- ምድብ (category): "Academic", "Facility", "Administrative", "Harassment", "Health", "IT", "Library", "Cafeteria", "Dormitory", "Other" ውስጥ አንዱ
- አስቸኳይነት (urgency): "low", "medium", "high", "critical" ውስጥ አንዱ

የጎደሉ መረጃዎች (missing_info):
- "ቦታ" - ልዩ ቦታ ካልተጠቀሰ
- "ቀን" - ቀን እና ሰዓት ካልተጠቀሰ  
- "ማስረጃ" - ማስረጃ ወይም ምሳሌ ካልተጠቀሰ
- "ተጽእኖ" - ችግሩ ያመጣው ተጽእኖ ካልተጠቀሰ

ምክሮች (suggestions) በአማርኛ:
- "ልዩ ቦታ ይጥቀሱ (ህንጻ፣ ክፍል ቁጥር)"
- "ቀን እና ሰዓት ያክሉ"
- "ስለ ችግሩ የበለጠ ዝርዝር ይስጡ"
- "ማስረጃ ወይም ምሳሌ ያክሉ"

JSON ብቻ መልስ፣ ሌላ ጽሑፍ አትጨምር።"""
        
        # English prompt
        return f"""Analyze this complaint and provide structured feedback in JSON format.

Complaint Text: "{text}"
Category: {category or 'Unknown'}
Language: {language}

Analyze and return ONLY valid JSON with this exact structure:
{{
    "completeness_score": <0-100>,
    "clarity_score": <0-100>,
    "missing_info": [list of missing elements like "location", "date", "evidence", "impact"],
    "suggestions": [list of 2-3 specific actionable suggestions],
    "tone": "<professional|angry|frustrated|neutral>",
    "detected_category": "<Academic|Facility|Administrative|Harassment|Health|IT|Library|Cafeteria|Dormitory|Other>",
    "urgency": "<low|medium|high|critical>"
}}

Evaluation criteria:
- Completeness: Does it include what, where, when, who, evidence?
- Clarity: Is it specific and easy to understand?
- Tone: Is it professional or emotional?
- Urgency: Based on keywords like "emergency", "urgent", "immediately"

Return ONLY the JSON, no other text."""
    
    def _parse_ai_response(self, response):
        """Parse AI response into structured data"""
        import json
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return self._get_fallback_analysis("")
        except:
            return self._get_fallback_analysis("")
    
    def _get_fallback_analysis(self, text):
        """Fallback analysis when AI fails"""
        word_count = len(text.split())
        has_location = any(word in text.lower() for word in ['building', 'room', 'library', 'cafeteria', 'dorm', 'ህንጻ', 'ክፍል', 'ቤተ መጻህፍት'])
        has_date = any(word in text.lower() for word in ['today', 'yesterday', 'monday', 'tuesday', 'january', 'december', 'ዛሬ', 'ትናንት', 'ሳምንት', 'ወር'])
        
        missing = []
        if not has_location:
            missing.append('location')
        if not has_date:
            missing.append('date')
        if word_count < 15:
            missing.append('detailed description')
        
        # More lenient scoring for 50% thresholds
        completeness = max(20, 100 - (len(missing) * 20))  # Start at 20%, lose 20% per missing item
        clarity = min(100, max(30, word_count * 4))  # More generous clarity scoring
        
        suggestions = []
        if not has_location:
            suggestions.append('Add specific location (building, room number)')
        if not has_date:
            suggestions.append('Include when this happened (date and time)')
        if word_count < 15:
            suggestions.append('Provide more details about the issue')
        
        return {
            'completeness_score': completeness,
            'clarity_score': clarity,
            'missing_info': missing,
            'suggestions': suggestions[:3],
            'tone': 'neutral',
            'detected_category': None,
            'urgency': 'medium'
        }


# Singleton instance
complaint_analyzer = ComplaintAnalyzer()