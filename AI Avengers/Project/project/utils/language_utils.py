import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class LanguageTranslator:
    def __init__(self):
        # Basic Dzongkha-English dictionary for common terms
        self.dzongkha_to_english = {
            # Government terms
            "གཞུང་": "government",
            "ལས་ཀ": "work/job",
            "ཁྲལ": "tax",
            "ཁྲིམས": "law",
            "རྩ་ཁྲིམས": "constitution",
            "འགྲུལ་བསྐྱོད": "tourism",
            "རིག་གཞུང་": "culture",
            "ཞབས་ཏོག": "service",
            "རོགས་པ": "help",
            "དྲི་བ": "question",
            "ལན": "answer",
            
            # Common phrases
            "ཁྱེད་རང་ལ་གསོལ་བ": "please",
            "ཐུགས་རྗེ་ཆེ": "thank you",
            "མི་གོ་བ": "don't understand",
            "རེད": "yes",
            "མིན": "no",
            "ག་པར": "where",
            "ག་ཅིར": "what",
            "ག་དུས": "when",
            "ག་རེ": "how"
        }
        
        self.english_to_dzongkha = {v: k for k, v in self.dzongkha_to_english.items()}
        
        # Common government responses in Dzongkha
        self.common_responses_dz = {
            "help": "ང་རང་གིས་ཁྱེད་རང་ལ་རོགས་པ་བྱེད་ཆོག",
            "not_understand": "མི་གོ་བ། དྲིས་ལན་བྱེད་མི་ཐུབ་པས་སླར་ཡང་འདྲི་རོགས།",
            "contact_office": "ཞིབ་ཕྲའི་གནས་ཚུལ་གྱི་དོན་ལུ་དབང་འཛིན་ལས་ཁུངས་ལུ་འབྲེལ་བ་འཐབ་རོགས།",
            "thank_you": "ཐུགས་རྗེ་ཆེ། རོགས་པ་བྱེད་ཐུབ་པར་དགའ་པོ་བྱུང་།"
        }
    
    def translate_dzongkha_to_english(self, text: str) -> str:
        """Translate Dzongkha text to English"""
        if not text or not text.strip():
            return text
        
        try:
            # Simple word-by-word translation for basic terms
            words = text.split()
            translated_words = []
            
            for word in words:
                # Remove common punctuation
                clean_word = word.strip('།')
                translated = self.dzongkha_to_english.get(clean_word, word)
                translated_words.append(translated)
            
            result = ' '.join(translated_words)
            logger.info(f"Translated DZ->EN: {text} -> {result}")
            return result
            
        except Exception as e:
            logger.error(f"Translation error DZ->EN: {str(e)}")
            return text
    
    def translate_english_to_dzongkha(self, text: str) -> str:
        """Translate English text to Dzongkha"""
        if not text or not text.strip():
            return text
        
        try:
            # For now, return basic translations for key terms
            # In production, this would use a proper translation model
            
            # Check for common phrases first
            text_lower = text.lower()
            
            if "thank you" in text_lower:
                return text.replace("thank you", "ཐུགས་རྗེ་ཆེ").replace("Thank you", "ཐུགས་རྗེ་ཆེ")
            
            if "help" in text_lower and "can" in text_lower:
                return "ང་རང་གིས་ཁྱེད་རང་ལ་རོགས་པ་བྱེད་ཆོག"
            
            if "sorry" in text_lower or "apologize" in text_lower:
                return "མི་གོ་བ། དྲིས་ལན་བྱེད་མི་ཐུབ་པས་སླར་ཡང་འདྲི་རོགས།"
            
            # Basic word replacement
            result = text
            for eng_word, dz_word in self.english_to_dzongkha.items():
                result = result.replace(eng_word, dz_word)
            
            logger.info(f"Translated EN->DZ: {text} -> {result}")
            return result
            
        except Exception as e:
            logger.error(f"Translation error EN->DZ: {str(e)}")
            return text
    
    def detect_language(self, text: str) -> str:
        """Detect if text is Dzongkha or English"""
        if not text:
            return "en"
        
        # Count Dzongkha characters (Tibetan Unicode block)
        dzongkha_chars = sum(1 for char in text if '\u0F00' <= char <= '\u0FFF')
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars == 0:
            return "en"
        
        dzongkha_ratio = dzongkha_chars / total_chars
        
        return "dz" if dzongkha_ratio > 0.3 else "en"
    
    def get_language_name(self, lang_code: str) -> Dict[str, str]:
        """Get language names in both languages"""
        names = {
            "en": {"en": "English", "dz": "དབྱིན་ཇི"},
            "dz": {"en": "Dzongkha", "dz": "རྫོང་ཁ"}
        }
        return names.get(lang_code, {"en": "Unknown", "dz": "མི་ཤེས"})