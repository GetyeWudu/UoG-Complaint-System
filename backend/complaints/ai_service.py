from textblob import TextBlob
from difflib import SequenceMatcher
import re
import logging

# Initialize sentiment analyzer (with fallback)
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    sentiment_analyzer = SentimentIntensityAnalyzer()
except ImportError:
    try:
        from vaderSentiment import SentimentIntensityAnalyzer
        sentiment_analyzer = SentimentIntensityAnalyzer()
    except ImportError:
        # Fallback: create a dummy analyzer if vaderSentiment is not available
        class DummySentimentAnalyzer:
            def polarity_scores(self, text):
                return {'compound': 0.0, 'pos': 0.0, 'neu': 1.0, 'neg': 0.0}
        sentiment_analyzer = DummySentimentAnalyzer()
        logging.warning("vaderSentiment not available, using dummy sentiment analyzer")

logger = logging.getLogger(__name__)

# Enhanced keyword lists (English + Amharic)
CRITICAL_KEYWORDS = [
    # English
    'danger', 'fire', 'broken glass', 'leak', 'flood', 'spark', 'smoke', 
    'stuck', 'lock', 'theft', 'blood', 'emergency', 'injury', 'accident',
    'assault', 'harassment', 'violence', 'explosion', 'gas leak',
    # Amharic (transliterated) - add actual Amharic Unicode if needed
    'አደጋ', 'እሳት', 'ደም', 'አስቸኳይ', 'ጥቃት', 'ወንጀል'
]

HIGH_KEYWORDS = [
    # English - truly urgent issues
    'urgent', 'critical', 'immediate', 'asap', 'right now', 'emergency',
    'security', 'safety', 'unsafe', 'hazard', 'dangerous',
    'not working and', 'completely broken', 'totally broken',
    # Amharic (transliterated)
    'አስቸኳይ', 'አደጋ'
]

MEDIUM_KEYWORDS = [
    # English - issues that need attention but not urgent
    'not working', 'broken', 'issue', 'problem', 'concern',
    'slow', 'dirty', 'smell', 'noise', 'wifi', 'internet', 'pest', 
    'rat', 'cockroach', 'tomorrow', 'next week', 'soon',
    'blurry', 'unclear', 'malfunctioning',
    # Amharic (transliterated)
    'አይሰራም', 'ተሰብሯል', 'ዝግተኛ', 'ቆሻሻ', 'ጥያቄ', 'ችግር'
]

LOW_KEYWORDS = [
    # English - minor issues or requests
    'suggestion', 'recommend', 'would be nice', 'could be better',
    'request', 'feedback', 'improvement', 'enhancement'
]


def analyze_urgency(text, language='en'):
    """
    Analyzes the complaint description to determine urgency.
    Returns: ('critical', 'high', 'medium', 'low'), confidence_score, reason
    """
    if not text:
        return 'low', 0.5, "No text provided"
    
    text_lower = text.lower()
    blob = TextBlob(text_lower)
    
    confidence = 0.5
    urgency = 'low'  # Default urgency
    reason_parts = []
    
    # 1. Keyword Search (most reliable)
    # Check for CRITICAL first
    for keyword in CRITICAL_KEYWORDS:
        if keyword in text_lower:
            reason_parts.append(f"Critical keyword: '{keyword}'")
            return 'critical', 0.9, "; ".join(reason_parts)
    
    # Check for HIGH urgency
    high_keyword_count = 0
    for keyword in HIGH_KEYWORDS:
        if keyword in text_lower:
            high_keyword_count += 1
            reason_parts.append(f"High urgency keyword: '{keyword}'")
    
    if high_keyword_count > 0:
        return 'high', 0.85, "; ".join(reason_parts)
    
    # Check for MEDIUM urgency
    medium_keyword_count = 0
    for keyword in MEDIUM_KEYWORDS:
        if keyword in text_lower:
            medium_keyword_count += 1
            if not reason_parts:  # Only add first match
                reason_parts.append(f"Medium urgency keyword: '{keyword}'")
    
    if medium_keyword_count > 0:
        confidence = 0.7
        urgency = 'medium'
    
    # Check for LOW urgency indicators
    low_keyword_count = 0
    for keyword in LOW_KEYWORDS:
        if keyword in text_lower:
            low_keyword_count += 1
            if not reason_parts:
                reason_parts.append(f"Low urgency keyword: '{keyword}'")
    
    if low_keyword_count > 0 and urgency == 'low':
        confidence = 0.75
        urgency = 'low'
    
    # 2. Sentiment Analysis
    sentiment_scores = sentiment_analyzer.polarity_scores(text)
    compound_score = sentiment_scores['compound']
    
    if compound_score < -0.6:  # Very negative
        if not reason_parts:
            urgency = 'high'
            confidence = 0.75
        reason_parts.append(f"Very negative sentiment (score: {compound_score:.2f})")
    elif compound_score < -0.3:  # Negative
        if urgency == 'low':
            urgency = 'medium'
            confidence = 0.65
        reason_parts.append(f"Negative sentiment (score: {compound_score:.2f})")
    
    # 3. TextBlob sentiment as backup
    if blob.sentiment.polarity < -0.5:
        if urgency == 'low':
            urgency = 'medium'
        reason_parts.append(f"TextBlob sentiment: {blob.sentiment.polarity:.2f}")
    
    # 4. Length and urgency indicators
    if len(text.split()) > 200:  # Long complaint might indicate seriousness
        if urgency == 'low':
            urgency = 'medium'
            confidence = 0.6
    
    reason = "; ".join(reason_parts) if reason_parts else "Default priority assessment"
    return urgency, confidence, reason


def analyze_sentiment(text):
    """
    Analyze sentiment of complaint text.
    Returns: sentiment_score (-1 to 1), sentiment_label, confidence
    """
    if not text:
        return 0.0, 'neutral', 0.5
    
    # Use VADER for better accuracy
    scores = sentiment_analyzer.polarity_scores(text)
    compound = scores['compound']
    
    # Determine label
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'
    
    confidence = abs(compound)  # Confidence based on how far from neutral
    
    return compound, label, confidence


def generate_summary(text, max_length=150):
    """
    Generate a concise summary of the complaint for quick triage.
    """
    if not text:
        return ""
    
    # Simple extractive summarization (first sentence + key info)
    sentences = text.split('.')
    
    if len(sentences) > 0:
        first_sentence = sentences[0].strip()
        if len(first_sentence) <= max_length:
            return first_sentence
        else:
            # Truncate first sentence
            return first_sentence[:max_length-3] + "..."
    
    # Fallback: truncate text
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def detect_duplicate(new_complaint_text, existing_complaints, threshold=0.7):
    """
    Detect if a new complaint is similar to existing ones.
    
    Args:
        new_complaint_text: Text of the new complaint
        existing_complaints: List of dicts with 'id', 'title', 'description', 'status'
        threshold: Similarity threshold (0-1)
    
    Returns:
        (is_duplicate: bool, similar_complaint_id: int or None, similarity_score: float)
    """
    if not new_complaint_text or not existing_complaints:
        return False, None, 0.0
    
    new_text_normalized = normalize_text(new_complaint_text)
    best_match = None
    best_score = 0.0
    
    for complaint in existing_complaints:
        # Skip closed/resolved complaints older than 30 days
        if complaint.get('status') in ['closed', 'resolved']:
            continue
        
        # Combine title and description for comparison
        existing_text = f"{complaint.get('title', '')} {complaint.get('description', '')}"
        existing_text_normalized = normalize_text(existing_text)
        
        # Calculate similarity
        similarity = calculate_similarity(new_text_normalized, existing_text_normalized)
        
        if similarity > best_score:
            best_score = similarity
            best_match = complaint.get('id')
    
    is_duplicate = best_score >= threshold
    return is_duplicate, best_match, best_score


def normalize_text(text):
    """Normalize text for comparison (lowercase, remove extra spaces)"""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    return text.strip()


def calculate_similarity(text1, text2):
    """Calculate similarity between two texts using SequenceMatcher"""
    return SequenceMatcher(None, text1, text2).ratio()


def translate_text(text, source_lang='am', target_lang='en'):
    """
    Translate text from source language to target language.
    Uses googletrans library with fallback.
    
    Returns: (translated_text, confidence_score, provider)
    """
    if not text:
        return text, 0.0, 'none'
    
    # If already in target language, return as-is
    if source_lang == target_lang:
        return text, 1.0, 'none'
    
    try:
        from googletrans import Translator
        translator = Translator()
        
        result = translator.translate(text, src=source_lang, dest=target_lang)
        # Confidence is not directly available, but we can estimate
        confidence = 0.85 if result.text and result.text != text else 0.0
        
        return result.text, confidence, 'googletrans'
    except Exception as e:
        # Fallback: return original text if translation fails
        logger.warning(f"Translation error: {e}")
        return text, 0.0, 'failed'


def detect_language(text):
    """
    Detect the language of the text.
    Returns: language_code, confidence
    """
    if not text:
        return 'en', 0.5
    
    try:
        from googletrans import Translator
        translator = Translator()
        result = translator.detect(text)
        # Normalize language code
        lang_code = result.lang
        if lang_code.startswith('am'):  # Amharic variants
            lang_code = 'am'
        elif lang_code.startswith('en'):
            lang_code = 'en'
        return lang_code, result.confidence
    except Exception as e:
        logger.warning(f"Language detection error: {e}")
        # Fallback: check for Amharic Unicode range
        if any('\u1200' <= char <= '\u137F' for char in text):
            return 'am', 0.7
        # Assume English
        return 'en', 0.5


def suggest_routing(category, sub_category, description, campus=None):
    """
    Suggest which department/user should handle this complaint.
    
    Returns: {
        'suggested_department': Department or None,
        'suggested_user': User or None,
        'confidence': float,
        'reason': str
    }
    """
    from accounts.models import Department, CustomUser
    
    suggestion = {
        'suggested_department': None,
        'suggested_user': None,
        'confidence': 0.5,
        'reason': 'Default routing'
    }
    
    if not category:
        return suggestion
    
    # Simple keyword-based routing suggestions
    description_lower = description.lower() if description else ''
    
    # IT/Network complaints
    if 'wifi' in description_lower or 'internet' in description_lower or 'network' in description_lower:
        it_dept = Department.objects.filter(name__icontains='IT').first() or \
                  Department.objects.filter(name__icontains='Information').first()
        if it_dept:
            suggestion['suggested_department'] = it_dept
            suggestion['confidence'] = 0.8
            suggestion['reason'] = 'IT/Network related issue'
    
    # Maintenance/Facility complaints
    elif 'broken' in description_lower or 'repair' in description_lower or 'maintenance' in description_lower:
        maint_dept = Department.objects.filter(name__icontains='Maintenance').first() or \
                     Department.objects.filter(name__icontains='Facility').first()
        if maint_dept:
            suggestion['suggested_department'] = maint_dept
            suggestion['confidence'] = 0.75
            suggestion['reason'] = 'Maintenance/Facility related issue'
    
    # Security complaints
    elif 'security' in description_lower or 'theft' in description_lower or 'safety' in description_lower:
        security_user = CustomUser.objects.filter(role='proctor').first()
        if security_user:
            suggestion['suggested_user'] = security_user
            suggestion['confidence'] = 0.85
            suggestion['reason'] = 'Security/Safety related issue'
    
    # Category-based routing
    if category.name.lower() in ['it', 'network', 'technology']:
        it_dept = Department.objects.filter(name__icontains='IT').first()
        if it_dept:
            suggestion['suggested_department'] = it_dept
            suggestion['confidence'] = 0.9
            suggestion['reason'] = f'Category: {category.name}'
    
    return suggestion