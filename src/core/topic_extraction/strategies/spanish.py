# src/core/topic_extraction/strategies/spanish.py
import re
from typing import List
from domain.entities import AnalyzedText, Topic, Language, SentimentLabel, BusinessCategory, TopicCategory, SPANISH_CATEGORIES
from .base import BaseTopicExtractor

class SpanishTopicExtractor(BaseTopicExtractor):
    """extraccion de temas para espanol - IMPLEMENTA LOGICA DE NEGOCIO"""
    
    def __init__(self, categories: List[TopicCategory] = None):
        self.categories = categories or SPANISH_CATEGORIES
        
        # Stop words específicas del espanol - PARTE DE LA LOGICA DE NEGOCIO
        self.stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero',
            'en', 'a', 'de', 'con', 'por', 'para', 'sin', 'sobre', 'entre', 'hacia'
        }
    
    @property
    def supported_language(self) -> Language:
        return Language.SPANISH
    
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
    
    def _text_matches_category(self, text: str, category: TopicCategory) -> bool:
        """LOGICA DE NEGOCIO: determinar si un texto coincide con una CategorIa"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in category.keywords)
    
    def _build_topics_from_matches(self, matches: dict) -> List[Topic]:
        """LOGICA DE NEGOCIO: construir temas a partir de coincidencias"""
        topics = []
        
        for category, texts in matches.items():
            if len(texts) >= 2:  # REGLA DE NEGOCIO: mínimo 2 menciones
                sentiment_dist = self._calculate_sentiment_distribution(texts)
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
    
    def _calculate_sentiment_distribution(self, texts: List[AnalyzedText]) -> Dict[SentimentLabel, int]:
        """Calcular distribucion de sentimientos"""
        distribution = {label: 0 for label in SentimentLabel}
        for text in texts:
            distribution[text.sentiment] += 1
        return distribution