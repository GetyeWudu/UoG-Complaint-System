"""
Smart AI-powered complaint validation
Detects and blocks invalid, spam, or inappropriate complaints
"""
import re
from difflib import SequenceMatcher
from textblob import TextBlob


class ComplaintValidator:
    """Validates complaint content before submission"""
    
    # Profanity/Insult keywords (English + Amharic transliterated)
    PROFANITY_KEYWORDS = [
        'fuck', 'shit', 'damn', 'bitch', 'asshole', 'bastard', 'idiot', 'stupid',
        'dumb', 'moron', 'retard', 'hate', 'kill', 'die', 'death',
        # Add Amharic insults if needed
    ]
    
    # Spam/Advertisement keywords
    SPAM_KEYWORDS = [
        'buy now', 'click here', 'free money', 'win prize', 'call now',
        'limited offer', 'act now', 'discount', 'sale', 'www.', 'http',
        'viagra', 'casino', 'lottery', 'bitcoin', 'crypto'
    ]
    
    # Minimum requirements
    MIN_TITLE_LENGTH = 5
    MIN_DESCRIPTION_LENGTH = 10
    MIN_WORDS = 3
    MAX_REPEATED_CHARS = 4  # e.g., "aaaa" is suspicious
    
    @staticmethod
    def validate_complaint(title, description, user=None):
        """
        Validate complaint content
        Returns: (is_valid: bool, error_message: str or None)
        """
        
        # 1. Check minimum length
        if len(title.strip()) < ComplaintValidator.MIN_TITLE_LENGTH:
            return False, f"Title too short. Minimum {ComplaintValidator.MIN_TITLE_LENGTH} characters required."
        
        if len(description.strip()) < ComplaintValidator.MIN_DESCRIPTION_LENGTH:
            return False, f"Description too short. Please provide more details (minimum {ComplaintValidator.MIN_DESCRIPTION_LENGTH} characters)."
        
        # 2. Check word count
        title_words = len(title.split())
        desc_words = len(description.split())
        
        if title_words < 2:
            return False, "Title must contain at least 2 words. Please write a clear title."
        
        if desc_words < ComplaintValidator.MIN_WORDS:
            return False, f"Description must contain at least {ComplaintValidator.MIN_WORDS} words. Please explain your issue clearly."
        
        # 3. Check for gibberish (excessive repeated characters)
        if ComplaintValidator._is_gibberish(title) or ComplaintValidator._is_gibberish(description):
            return False, "Your complaint appears to contain random or meaningless text. Please write a clear, meaningful complaint."
        
        # 4. Check for profanity/insults
        combined_text = (title + " " + description).lower()
        for word in ComplaintValidator.PROFANITY_KEYWORDS:
            if word in combined_text:
                return False, "Your complaint contains inappropriate language. Please be respectful and professional."
        
        # 5. Check for spam/advertisements
        for keyword in ComplaintValidator.SPAM_KEYWORDS:
            if keyword in combined_text:
                return False, "Your submission appears to be spam or advertisement. This system is for genuine complaints only."
        
        # 6. Check for excessive special characters (spam indicator)
        special_char_ratio = ComplaintValidator._special_char_ratio(description)
        if special_char_ratio > 0.3:  # More than 30% special chars
            return False, "Your complaint contains too many special characters. Please write in normal text."
        
        # 7. Check for all caps (shouting/spam)
        if title.isupper() and len(title) > 10:
            return False, "Please don't write in ALL CAPS. Use normal capitalization."
        
        # 8. Check for meaningful content (vowel ratio test)
        if not ComplaintValidator._has_meaningful_content(description):
            return False, "Your complaint doesn't appear to contain meaningful text. Please write a clear description of your issue."
        
        # 9. Check for duplicate (if user provided)
        if user:
            is_duplicate, similar_complaint = ComplaintValidator._check_duplicate(title, description, user)
            if is_duplicate:
                return False, f"You have already submitted a similar complaint (Tracking ID: {similar_complaint.tracking_id}). Please check your existing complaints."
        
        # All checks passed
        return True, None
    
    @staticmethod
    def _is_gibberish(text):
        """Detect gibberish by checking for excessive repeated characters"""
        # Check for patterns like "aaaa", "bbbb", "lnwvnvw"
        
        # Pattern 1: Same character repeated many times
        if re.search(r'(.)\1{' + str(ComplaintValidator.MAX_REPEATED_CHARS) + ',}', text):
            return True
        
        # Pattern 2: Very low vowel ratio (gibberish usually has few vowels)
        vowels = len(re.findall(r'[aeiouAEIOU]', text))
        consonants = len(re.findall(r'[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ]', text))
        
        if consonants > 0:
            vowel_ratio = vowels / (vowels + consonants)
            if vowel_ratio < 0.15:  # Less than 15% vowels = likely gibberish
                return True
        
        # Pattern 3: Check for keyboard mashing (adjacent keys)
        keyboard_patterns = ['qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', 'plokij']
        text_lower = text.lower()
        for pattern in keyboard_patterns:
            if pattern in text_lower or pattern[::-1] in text_lower:
                return True
        
        return False
    
    @staticmethod
    def _special_char_ratio(text):
        """Calculate ratio of special characters to total characters"""
        special_chars = len(re.findall(r'[^a-zA-Z0-9\s]', text))
        total_chars = len(text.replace(' ', ''))
        return special_chars / total_chars if total_chars > 0 else 0
    
    @staticmethod
    def _has_meaningful_content(text):
        """Check if text has meaningful content (not just random chars)"""
        # Remove spaces and special chars
        clean_text = re.sub(r'[^a-zA-Z]', '', text)
        
        if len(clean_text) < 5:
            return False
        
        # Check vowel ratio
        vowels = len(re.findall(r'[aeiouAEIOU]', clean_text))
        total = len(clean_text)
        
        vowel_ratio = vowels / total if total > 0 else 0
        
        # Meaningful text usually has 20-50% vowels
        return 0.15 <= vowel_ratio <= 0.7
    
    @staticmethod
    def _check_duplicate(title, description, user):
        """Check if user has submitted similar complaint recently"""
        from .models import Complaint
        from datetime import timedelta
        from django.utils import timezone
        
        # Get user's recent complaints (last 30 days)
        recent_date = timezone.now() - timedelta(days=30)
        recent_complaints = Complaint.objects.filter(
            submitter=user,
            created_at__gte=recent_date,
            status__in=['new', 'assigned', 'in_progress', 'pending']  # Only check open complaints
        )
        
        # Check similarity
        for complaint in recent_complaints:
            # Compare titles
            title_similarity = SequenceMatcher(None, title.lower(), complaint.title.lower()).ratio()
            desc_similarity = SequenceMatcher(None, description.lower(), complaint.description.lower()).ratio()
            
            # If very similar (>80% match), consider duplicate
            if title_similarity > 0.8 or desc_similarity > 0.8:
                return True, complaint
        
        return False, None


def validate_complaint_content(title, description, user=None):
    """
    Convenience function to validate complaint
    Returns: (is_valid, error_message)
    """
    return ComplaintValidator.validate_complaint(title, description, user)



# File validation functions
def validate_file_size(file):
    """Validate file size (max 10MB)"""
    from django.conf import settings
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 10485760)  # 10MB default
    
    if file.size > max_size:
        from rest_framework.exceptions import ValidationError
        raise ValidationError(f'File size exceeds maximum allowed size of {max_size / 1024 / 1024:.1f}MB')


def validate_file_extension(file):
    """Validate file extension"""
    import os
    from django.conf import settings
    from rest_framework.exceptions import ValidationError
    
    allowed_extensions = getattr(settings, 'ALLOWED_FILE_TYPES', 'jpg,jpeg,png,gif,pdf,doc,docx').split(',')
    
    ext = os.path.splitext(file.name)[1][1:].lower()  # Get extension without dot
    
    if ext not in allowed_extensions:
        raise ValidationError(f'File type .{ext} is not allowed. Allowed types: {", ".join(allowed_extensions)}')


def sanitize_filename(filename):
    """Sanitize filename to prevent security issues"""
    import os
    import re
    
    # Get the file extension
    name, ext = os.path.splitext(filename)
    
    # Remove any path components
    name = os.path.basename(name)
    
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    
    # Limit length
    name = name[:100]
    
    return f"{name}{ext}"
