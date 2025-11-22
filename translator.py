"""
Translation service for multi-language support
"""
from typing import Optional
import requests
import json

# Language codes mapping
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'tr': 'Turkish',
    'pl': 'Polish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'cs': 'Czech',
    'ro': 'Romanian',
    'hu': 'Hungarian',
    'el': 'Greek',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'ms': 'Malay',
    'uk': 'Ukrainian',
    'bg': 'Bulgarian',
    'hr': 'Croatian',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'et': 'Estonian',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
}


class Translator:
    """Translation service using LibreTranslate (free, no API key needed)"""
    
    # Using LibreTranslate public API (free, no key required)
    BASE_URL = "https://libretranslate.de/translate"
    
    def __init__(self):
        self.supported_languages = LANGUAGES
    
    def translate(self, text: str, target_lang: str = 'en', source_lang: str = 'auto') -> Optional[str]:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_lang: Target language code (default: 'en')
            source_lang: Source language code or 'auto' for auto-detect
            
        Returns:
            Translated text or None if error
        """
        if target_lang == 'en' or not text:
            return text
        
        try:
            # Use LibreTranslate API
            response = requests.post(
                self.BASE_URL,
                data={
                    'q': text,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('translatedText', text)
            else:
                # Fallback: try alternative method
                return self._translate_fallback(text, target_lang)
                
        except Exception as e:
            print(f"Translation error: {e}")
            # Fallback to simple method
            return self._translate_fallback(text, target_lang)
    
    def _translate_fallback(self, text: str, target_lang: str) -> str:
        """Fallback translation using MyMemory API"""
        try:
            url = f"https://api.mymemory.translated.net/get"
            params = {
                'q': text,
                'langpair': f'en|{target_lang}'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('responseStatus') == 200:
                    return data['responseData']['translatedText']
        except:
            pass
        return text
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the text.
        
        Args:
            text: Text to detect
            
        Returns:
            Language code
        """
        try:
            # Simple detection based on character sets
            if any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' for char in text):
                return 'ja'  # Japanese
            elif any('\u4e00' <= char <= '\u9fff' for char in text):
                return 'zh'  # Chinese
            elif any('\uAC00' <= char <= '\uD7A3' for char in text):
                return 'ko'  # Korean
            elif any('\u0600' <= char <= '\u06FF' for char in text):
                return 'ar'  # Arabic
            elif any('\u0900' <= char <= '\u097F' for char in text):
                return 'hi'  # Hindi
            elif any('\u0E00' <= char <= '\u0E7F' for char in text):
                return 'th'  # Thai
            else:
                return 'en'  # Default to English
        except:
            return 'en'
    
    def translate_response(self, response: str, target_lang: str, place_name: str = None) -> str:
        """
        Translate the response while preserving place names.
        
        Args:
            response: Response text to translate
            target_lang: Target language code
            place_name: Place name to preserve (optional)
            
        Returns:
            Translated response
        """
        if target_lang == 'en' or not response:
            return response
        
        # Extract place name from response if not provided
        if place_name:
            # Temporarily replace place name with placeholder
            placeholder = f"__PLACE__{hash(place_name)}__"
            response = response.replace(place_name, placeholder)
        
        # Translate
        translated = self.translate(response, target_lang)
        
        # Restore place name
        if place_name:
            translated = translated.replace(placeholder, place_name)
        
        return translated
    
    def get_language_name(self, lang_code: str) -> str:
        """Get language name from code"""
        return self.supported_languages.get(lang_code, lang_code)


# Global translator instance
translator = Translator()

