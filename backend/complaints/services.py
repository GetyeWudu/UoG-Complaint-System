from textblob import TextBlob

def analyze_complaint_local(title, description):
    text = f"{title} {description}".lower()
    
    # 1. Auto-Categorization
    category = "other"
    if any(word in text for word in ['grade', 'exam', 'class', 'lecturer', 'course']):
        category = 'academic'
    elif any(word in text for word in ['water', 'light', 'broken', 'leak', 'toilet', 'wifi', 'door', 'bed']):
        category = 'facility'
    elif any(word in text for word in ['fee', 'payment', 'money', 'tuition', 'cost']):
        category = 'finance'

    # 2. Sentiment & Urgency (with Safety Try/Except)
    urgency = 'low'
    polarity = 0.0
    
    try:
        blob = TextBlob(description)
        polarity = blob.sentiment.polarity
        if polarity < -0.5:
            urgency = 'medium'
    except:
        # If AI fails (e.g., missing files), default to 0
        polarity = 0.0

    # 3. Keyword Override (Works even if AI fails)
    critical_words = ['danger', 'fire', 'spark', 'blood', 'threat', 'emergency', 'unsafe', 'electric']
    if any(word in text for word in critical_words):
        urgency = 'high'

    return {
        "category_detected": category,
        "urgency_score": urgency,
        "sentiment_polarity": round(polarity, 2),
        "ai_model": "Local-TextBlob-Safe"
    }
