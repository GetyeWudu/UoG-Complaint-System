"""
AI-powered complaint validation system
Detects spam, inappropriate content, duplicates, and validates complaints
"""
import re
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ComplaintValidator:
    """AI-powered complaint validation"""
    
    # Spam/invalid indicators
    SPAM_KEYWORDS = [
        'viagra', 'casino', 'lottery', 'prize', 'winner', 'click here',
        'buy now', 'limited offer', 'act now', 'free money', 'get rich',
        'work from home', 'make money fast', 'no experience needed'
    ]
    
    # Inappropriate content indicators
    INAPPROPRIATE_KEYWORDS = [
        'hate', 'kill', 'bomb', 'weapon', 'violence', 'threat',
        # Add more as needed
    ]
    
    # Valid complaint indicators
    VALID_COMPLAINT_KEYWORDS = [
        'broken', 'not working', 'damaged', 'issue', 'problem', 'faulty',
        'leaking', 'dirty', 'unsafe', 'missing', 'stolen', 'harassment',
        'discrimination', 'unfair', 'delay', 'cancelled', 'poor', 'bad',
        'noise', 'smell', 'cold', 'hot', 'dark', 'light', 'water', 'electricity',
        'internet', 'wifi', 'computer', 'projector', 'chair', 'desk', 'door',
        'window', 'toilet', 'shower', 'food', 'service', 'staff', 'teacher',
        'grade', 'exam', 'assignment', 'library', 'dormitory', 'cafeteria'
    ]
    
    def __init__(self):
        self.min_length = 10  # Minimum complaint length
        self.max_length = 5000  # Maximum complaint length
    
    def validate_complaint(self, title: str, description: str) -> Dict:
        """
        Validate a complaint using AI-like heuristics
        
        Returns:
            {
                'is_valid': bool,
                'confidence': float (0-1),
                'reason': str,
                'flags': list,
                'suggestions': list
            }
        """
        flags = []
        suggestions = []
        confidence = 1.0
        
        # Combine title and description for analysis
        full_text = f"{title} {description}".lower()
        
        # Check 1: Length validation
        if len(description) < self.min_length:
            flags.append('too_short')
            suggestions.append('Please provide more details about your complaint')
            confidence -= 0.3
        
        if len(description) > self.max_length:
            flags.append('too_long')
            suggestions.append('Please keep your complaint concise')
            confidence -= 0.2
        
        # Check 2: Spam detection
        spam_score = self._detect_spam(full_text)
        if spam_score > 0.5:
            flags.append('potential_spam')
            suggestions.append('This looks like spam or advertising')
            confidence -= 0.5
        
        # Check 3: Inappropriate content
        inappropriate_score = self._detect_inappropriate(full_text)
        if inappropriate_score > 0.3:
            flags.append('inappropriate_content')
            suggestions.append('Please use appropriate language')
            confidence -= 0.4
        
        # Check 4: Gibberish detection
        if self._is_gibberish(full_text):
            flags.append('gibberish')
            suggestions.append('Please write a clear, meaningful complaint')
            confidence -= 0.6
        
        # Check 5: Valid complaint indicators
        validity_score = self._check_validity(full_text)
        if validity_score < 0.3:
            flags.append('unclear_complaint')
            suggestions.append('Please clearly describe the issue you are facing')
            confidence -= 0.3
        
        # Check 6: Excessive caps or punctuation
        if self._has_excessive_caps(full_text):
            flags.append('excessive_caps')
            suggestions.append('Please avoid writing in ALL CAPS')
            confidence -= 0.1
        
        if self._has_excessive_punctuation(full_text):
            flags.append('excessive_punctuation')
            suggestions.append('Please use normal punctuation')
            confidence -= 0.1
        
        # Determine if valid
        is_valid = confidence > 0.5 and 'potential_spam' not in flags
        
        # Generate reason
        if is_valid:
            reason = 'Complaint appears valid'
        else:
            reason = self._generate_rejection_reason(flags)
        
        return {
            'is_valid': is_valid,
            'confidence': max(0.0, min(1.0, confidence)),
            'reason': reason,
            'flags': flags,
            'suggestions': suggestions,
            'spam_score': spam_score,
            'validity_score': validity_score
        }
    
    def _detect_spam(self, text: str) -> float:
        """Detect spam indicators (0-1 score)"""
        spam_count = sum(1 for keyword in self.SPAM_KEYWORDS if keyword in text)
        
        # Check for excessive links
        url_count = len(re.findall(r'http[s]?://|www\.', text))
        
        # Check for excessive numbers (phone numbers, etc.)
        number_density = len(re.findall(r'\d{3,}', text)) / max(len(text.split()), 1)
        
        spam_score = (spam_count * 0.3) + (url_count * 0.2) + (number_density * 0.5)
        return min(1.0, spam_score)
    
    def _detect_inappropriate(self, text: str) -> float:
        """Detect inappropriate content (0-1 score)"""
        inappropriate_count = sum(1 for keyword in self.INAPPROPRIATE_KEYWORDS if keyword in text)
        return min(1.0, inappropriate_count * 0.4)
    
    def _is_gibberish(self, text: str) -> bool:
        """Detect gibberish text"""
        words = text.split()
        if len(words) < 3:
            return True
        
        # Check for excessive consonants
        consonant_ratio = len(re.findall(r'[bcdfghjklmnpqrstvwxyz]{5,}', text)) / max(len(words), 1)
        if consonant_ratio > 0.3:
            return True
        
        # Check for repeated characters
        if re.search(r'(.)\1{4,}', text):
            return True
        
        # Check for very short words
        short_word_ratio = sum(1 for word in words if len(word) <= 2) / len(words)
        if short_word_ratio > 0.7:
            return True
        
        return False
    
    def _check_validity(self, text: str) -> float:
        """Check for valid complaint indicators (0-1 score)"""
        valid_count = sum(1 for keyword in self.VALID_COMPLAINT_KEYWORDS if keyword in text)
        
        # Bonus for question marks (asking for help)
        has_question = '?' in text
        
        # Bonus for specific details (numbers, locations)
        has_details = bool(re.search(r'\d+|room|building|floor|block', text))
        
        validity_score = (valid_count * 0.2) + (0.2 if has_question else 0) + (0.2 if has_details else 0)
        return min(1.0, validity_score)
    
    def _has_excessive_caps(self, text: str) -> bool:
        """Check for excessive capital letters"""
        if len(text) < 10:
            return False
        caps_ratio = sum(1 for c in text if c.isupper()) / len(text)
        return caps_ratio > 0.5
    
    def _has_excessive_punctuation(self, text: str) -> bool:
        """Check for excessive punctuation"""
        punct_count = len(re.findall(r'[!?]{3,}', text))
        return punct_count > 2
    
    def _generate_rejection_reason(self, flags: list) -> str:
        """Generate human-readable rejection reason"""
        reasons = {
            'too_short': 'Complaint is too short',
            'too_long': 'Complaint is too long',
            'potential_spam': 'Appears to be spam or advertising',
            'inappropriate_content': 'Contains inappropriate content',
            'gibberish': 'Text appears to be gibberish',
            'unclear_complaint': 'Complaint is unclear or not specific',
            'excessive_caps': 'Excessive use of capital letters',
            'excessive_punctuation': 'Excessive punctuation'
        }
        
        main_flags = [f for f in flags if f in ['potential_spam', 'inappropriate_content', 'gibberish']]
        if main_flags:
            return reasons.get(main_flags[0], 'Invalid complaint')
        
        if flags:
            return reasons.get(flags[0], 'Invalid complaint')
        
        return 'Complaint does not meet validation criteria'
    
    def check_duplicate(self, title: str, description: str, existing_complaints: list) -> Dict:
        """
        Check if complaint is a duplicate
        
        Args:
            title: New complaint title
            description: New complaint description
            existing_complaints: List of existing complaints (dicts with 'title' and 'description')
        
        Returns:
            {
                'is_duplicate': bool,
                'confidence': float,
                'similar_complaints': list
            }
        """
        if not existing_complaints:
            return {'is_duplicate': False, 'confidence': 0.0, 'similar_complaints': []}
        
        new_text = f"{title} {description}".lower()
        new_words = set(new_text.split())
        
        similar_complaints = []
        
        for complaint in existing_complaints:
            existing_text = f"{complaint.get('title', '')} {complaint.get('description', '')}".lower()
            existing_words = set(existing_text.split())
            
            # Calculate similarity (Jaccard similarity)
            intersection = len(new_words & existing_words)
            union = len(new_words | existing_words)
            similarity = intersection / union if union > 0 else 0
            
            if similarity > 0.6:
                similar_complaints.append({
                    'id': complaint.get('id'),
                    'tracking_id': complaint.get('tracking_id'),
                    'title': complaint.get('title'),
                    'similarity': similarity
                })
        
        is_duplicate = len(similar_complaints) > 0 and similar_complaints[0]['similarity'] > 0.8
        confidence = similar_complaints[0]['similarity'] if similar_complaints else 0.0
        
        return {
            'is_duplicate': is_duplicate,
            'confidence': confidence,
            'similar_complaints': sorted(similar_complaints, key=lambda x: x['similarity'], reverse=True)[:3]
        }


# Singleton instance
validator = ComplaintValidator()


def validate_complaint(title: str, description: str) -> Dict:
    """Convenience function to validate a complaint"""
    return validator.validate_complaint(title, description)


def check_duplicate(title: str, description: str, existing_complaints: list) -> Dict:
    """Convenience function to check for duplicates"""
    return validator.check_duplicate(title, description, existing_complaints)
