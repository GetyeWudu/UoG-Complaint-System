"""
Translation service for handling Amharic/English translations
"""
from .ai_service import translate_text, detect_language
from .models import Complaint, ComplaintTranslation
from django.utils import timezone


def process_complaint_translation(complaint):
    """
    Process translation for a complaint if it's in Amharic.
    Updates complaint with translated text and metadata.
    """
    if not complaint:
        return
    
    # Detect language if not set
    if not complaint.language or complaint.language == 'en':
        detected_lang, confidence = detect_language(complaint.description)
        complaint.language = detected_lang if confidence > 0.7 else 'en'
    
    # If complaint is in Amharic, translate to English
    if complaint.language == 'am':
        # Translate title
        if not complaint.title_translated:
            title_translated, title_conf = translate_text(
                complaint.title, 
                source_lang='am', 
                target_lang='en'
            )
            complaint.title_translated = title_translated
            complaint.translation_confidence = title_conf
        
        # Translate description
        if not complaint.description_translated:
            desc_translated, desc_conf = translate_text(
                complaint.description,
                source_lang='am',
                target_lang='en'
            )
            complaint.description_translated = desc_translated
            # Use average confidence
            if complaint.translation_confidence:
                complaint.translation_confidence = (
                    complaint.translation_confidence + desc_conf
                ) / 2
            else:
                complaint.translation_confidence = desc_conf
        
        complaint.translation_provider = 'google_translate'
        complaint.save()


def get_complaint_display_text(complaint, user_language='en'):
    """
    Get complaint text in user's preferred language.
    Returns dict with title and description.
    """
    if not complaint:
        return {'title': '', 'description': ''}
    
    # If user wants Amharic and complaint is in Amharic, return original
    if user_language == 'am' and complaint.language == 'am':
        return {
            'title': complaint.title,
            'description': complaint.description,
            'is_translated': False
        }
    
    # If user wants English and complaint is in Amharic, return translation
    if user_language == 'en' and complaint.language == 'am':
        return {
            'title': complaint.title_translated or complaint.title,
            'description': complaint.description_translated or complaint.description,
            'is_translated': bool(complaint.title_translated or complaint.description_translated),
            'original_language': 'am',
            'translation_confidence': complaint.translation_confidence
        }
    
    # Default: return original (English)
    return {
        'title': complaint.title,
        'description': complaint.description,
        'is_translated': False
    }


def create_manual_translation(complaint, translated_by, title_translated, 
                             description_translated, notes=''):
    """
    Create a manual translation by admin.
    This overrides auto-translation.
    """
    translation = ComplaintTranslation.objects.create(
        complaint=complaint,
        translated_by=translated_by,
        title_translated=title_translated,
        description_translated=description_translated,
        from_language=complaint.language,
        to_language='en',
        notes=notes
    )
    
    # Update complaint with manual translation
    complaint.title_translated = title_translated
    complaint.description_translated = description_translated
    complaint.translation_confidence = 1.0  # Manual translations are 100% confident
    complaint.translation_provider = 'manual'
    complaint.save()
    
    return translation

