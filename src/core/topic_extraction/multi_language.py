from typing import List, Dict
from domain.entities import AnalyzedText, Topic, Language
from .base import BaseTopicExtractor

class MultiLanguageTopicExtractor(BaseTopicExtractor):
    """Coordinador que delega a extractores específicos por idioma"""
    
    def __init__(self):
        self.extractors: Dict[Language, BaseTopicExtractor] = {}
        self._setup_extractors()
    
    def _setup_extractors(self):
        """Configurar extractores disponibles"""
        try:
            from .strategies.spanish import SpanishTopicExtractor
            from .strategies.english import EnglishTopicExtractor
            
            self.extractors[Language.SPANISH] = SpanishTopicExtractor()
            self.extractors[Language.ENGLISH] = EnglishTopicExtractor()
            
        except ImportError as e:
            print(f"Warning: Some topic extractors not available: {e}")
    
    @property
    def supported_language(self) -> Language:
        return Language.AUTO  # Soporta múltiples idiomas
    
    def extract(self, texts: List[AnalyzedText]) -> List[Topic]:
        """Extraer temas agrupando por idioma"""
        # Agrupar textos por idioma
        texts_by_language: Dict[Language, List[AnalyzedText]] = {}
        for text in texts:
            if text.language not in texts_by_language:
                texts_by_language[text.language] = []
            texts_by_language[text.language].append(text)
        
        # Extraer temas por idioma
        all_topics = []
        for language, language_texts in texts_by_language.items():
            if language in self.extractors:
                language_topics = self.extractors[language].extract(language_texts)
                all_topics.extend(language_topics)
        
        return all_topics