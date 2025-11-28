from textblob import TextBlob

def analyze_urgency(text):
    """
    Analyzes the complaint description to determine urgency.
    Returns: 'high', 'medium', or 'low'
    """
    blob = TextBlob(text.lower())
    
    # 1. Keyword Search (The most reliable method for Maintenance)
    high_keywords = ['danger', 'fire', 'broken glass', 'leak', 'flood', 'spark', 'smoke', 'stuck', 'lock', 'theft', 'blood', 'emergency']
    medium_keywords = ['not working', 'slow', 'dirty', 'smell', 'noise', 'wifi', 'internet', 'pest', 'rat', 'cockroach']
    
    # Check for keywords
    for word in high_keywords:
        if word in blob.words:
            return 'high'
            
    for word in medium_keywords:
        if word in blob.words:
            return 'medium'

    # 2. Sentiment Analysis (Optional backup)
    # If the sentiment is extremely negative (angry student), bump priority
    if blob.sentiment.polarity < -0.5:
        return 'medium'

    return 'low'