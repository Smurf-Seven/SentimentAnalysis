# src/core/topic_extraction/strategies/english.py
from .spanish import SpanishTopicExtractor
from domain.entities import Language, ENGLISH_CATEGORIES
from .base import BaseTopicExtractor

class EnglishTopicExtractor(BaseTopicExtractor):
    """extraccion de temas para inglés - IMPLEMENTA LOGICA DE NEGOCIO"""
    
    def __init__(self, categories = None):
        self.categories = categories or ENGLISH_CATEGORIES
        
        # Stop words específicas del inglés - PARTE DE LA LOGICA DE NEGOCIO
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
        }
    
    @property
    def supported_language(self) -> Language:
        return Language.ENGLISH
    
    def extract(self, texts: List[AnalyzedText]) -> List[Topic]:
        """Extraer temas - LOGICA DE NEGOCIO CENTRAL"""
        topics_by_category = {}
        
        for text in texts:
            for category in self.categories:
                if self._text_matches_category(text.text, category):
                    if category.category not in topics_by_category:
                        topics_by_category[category.category] = []
                    topics_by_category[category.category].append(text)
        
        return self._build_topics_from_matches(topics_by_category)
    
    def _text_matches_category(self, text: str, category) -> bool:
        """LOGICA DE NEGOCIO: determinar si un texto coincide con una CategorIa"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in category.keywords)
    
    def _build_topics_from_matches(self, matches: dict) -> List[Topic]:
        """LOGICA DE NEGOCIO: construir temas a partir de coincidencias"""
        topics = []
        
        for category, texts in matches.items():
            if len(texts) >= 2:  # REGLA DE NEGOCIO: mínimo 2 menciones
                from .spanish import SpanishTopicExtractor
                sentiment_dist = SpanishTopicExtractor._calculate_sentiment_distribution(self, texts)
                examples = [t.text[:80] + "..." for t in texts[:3]]
                
                topic = Topic(
                    name=category.value,
                    category=category,
                    frequency=len(texts),
                    sentiment_distribution=sentiment_dist,
                    examples=examples,
                    language=self.supported_language
                )
                topics.append(topic)
        
        return topics