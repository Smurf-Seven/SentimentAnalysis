from abc import ABC, abstractmethod
from typing import List, Dict
from domain.entities import AnalyzedText, Topic, Language, SentimentLabel

class BaseTopicExtractor(ABC):
    """Interface para estrategias de extraccion de temas"""
    
    @property
    @abstractmethod
    def supported_language(self) -> Language:
        """Idioma que soporta esta estrategia"""
        pass
    
    @abstractmethod
    def extract(self, texts: List[AnalyzedText]) -> List[Topic]:
        """Extraer temas de textos analizados"""
        pass
    
    def _calculate_sentiment_distribution(self, texts: List[AnalyzedText]) -> Dict[SentimentLabel, int]:
        """Calcular distribucion de sentimientos"""
        distribution = {label: 0 for label in SentimentLabel}
        for text in texts:
            distribution[text.sentiment] += 1
        return distribution