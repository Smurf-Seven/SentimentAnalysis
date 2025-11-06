from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class Language(Enum):
    SPANISH = "es"
    ENGLISH = "en"
    AUTO = "auto"

class SentimentLabel(Enum):
    VERY_NEGATIVE = "1 star"
    NEGATIVE = "2 stars" 
    NEUTRAL = "3 stars"
    POSITIVE = "4 stars"
    VERY_POSITIVE = "5 stars"

@dataclass
class AnalyzedText:
    """Texto analizado con sentimiento"""
    text: str
    sentiment: SentimentLabel
    confidence: float
    language: Language
    aspects: List[str] = None
    
    def __post_init__(self):
        if self.aspects is None:
            self.aspects = []

@dataclass
class Topic:
    """Tema detectado con métricas"""
    name: str
    category: str
    frequency: int
    sentiment_distribution: Dict[SentimentLabel, int]
    examples: List[str]
    language: Language
    
    @property
    def negative_ratio(self) -> float:
        """Ratio de menciones negativas"""
        total = sum(self.sentiment_distribution.values())
        negatives = (self.sentiment_distribution.get(SentimentLabel.VERY_NEGATIVE, 0) +
                    self.sentiment_distribution.get(SentimentLabel.NEGATIVE, 0))
        return negatives / total if total > 0 else 0.0

@dataclass
class AnalysisResult:
    """Resultado completo del análisis"""
    analyzed_texts: List[AnalyzedText]
    topics: List[Topic]
    language_breakdown: Dict[Language, int]