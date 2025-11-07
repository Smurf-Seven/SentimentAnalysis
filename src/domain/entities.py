# src/domain/entities.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class Language(Enum):
    SPANISH = "es"
    ENGLISH = "en"
    AUTO = "auto"

class BusinessCategory(Enum):
    PRODUCT = "producto"
    SERVICE = "servicio"
    DELIVERY = "entrega" 
    PRICE = "precio"

class SentimentLabel(Enum):
    VERY_NEGATIVE = "1 star"
    NEGATIVE = "2 stars"
    NEUTRAL = "3 stars"
    POSITIVE = "4 stars"
    VERY_POSITIVE = "5 stars"

@dataclass
class TopicCategory:
    """CategorIa de negocio con sus palabras clave - ENTIDAD DE DOMINIO"""
    category: BusinessCategory
    keywords: List[str]
    language: Language
    
    def __post_init__(self):
        # Validacion de dominio
        if not self.keywords:
            raise ValueError("Una CategorIa debe tener palabras clave")

@dataclass
class AnalyzedText:
    """Texto analizado - ENTIDAD DE DOMINIO"""
    text: str
    sentiment: SentimentLabel
    confidence: float
    language: Language
    
    @classmethod
    def from_legacy(cls, legacy_data: Dict[str, Any]) -> 'AnalyzedText':
        """Factory method para crear desde formato legacy"""
        sentiment_map = {
            '1 star': SentimentLabel.VERY_NEGATIVE,
            '2 stars': SentimentLabel.NEGATIVE,
            '3 stars': SentimentLabel.NEUTRAL, 
            '4 stars': SentimentLabel.POSITIVE,
            '5 stars': SentimentLabel.VERY_POSITIVE
        }
        
        # Deteccion simple de idioma
        text = legacy_data.get('text', '')
        spanish_indicators = ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es']
        english_indicators = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on']
        
        spanish_count = sum(1 for word in spanish_indicators if word in text.lower())
        english_count = sum(1 for word in english_indicators if word in text.lower())
        language = Language.SPANISH if spanish_count > english_count else Language.ENGLISH
        
        return cls(
            text=text,
            sentiment=sentiment_map.get(legacy_data.get('sentiment', '3 stars'), SentimentLabel.NEUTRAL),
            confidence=legacy_data.get('confidence', 0.5),
            language=language
        )

@dataclass
class Topic:
    """Tema detectado - ENTIDAD DE DOMINIO"""
    name: str
    category: BusinessCategory
    frequency: int
    sentiment_distribution: Dict[SentimentLabel, int]
    examples: List[str]
    language: Language
    
    @property
    def negative_ratio(self) -> float:
        """Metrica de negocio calculada - PARTE DEL DOMINIO"""
        total = sum(self.sentiment_distribution.values())
        negatives = (self.sentiment_distribution.get(SentimentLabel.VERY_NEGATIVE, 0) +
                    self.sentiment_distribution.get(SentimentLabel.NEGATIVE, 0))
        return negatives / total if total > 0 else 0.0
    
    def to_legacy_dict(self) -> Dict[str, Any]:
        """Convertir a formato legacy - RESPONSABILIDAD DEL DOMINIO"""
        return {
            'name': self.name,
            'category': self.category.value,
            'frequency': self.frequency,
            'negative_ratio': self.negative_ratio,
            'examples': self.examples,
            'language': self.language.value
        }

# DEFINICIONES CENTRALIZADAS DE CATEGORiAS DE NEGOCIO
SPANISH_CATEGORIES = [
    TopicCategory(
        category=BusinessCategory.PRODUCT,
        keywords=['producto', 'calidad', 'funcion', 'diseno', 'rendimiento', 'material', 'durabilidad'],
        language=Language.SPANISH
    ),
    TopicCategory(
        category=BusinessCategory.SERVICE,
        keywords=['servicio', 'atencion', 'soporte', 'asesoramiento', 'trato', 'empleado', 'vendedor'],
        language=Language.SPANISH
    ),
    TopicCategory(
        category=BusinessCategory.DELIVERY,
        keywords=['entrega', 'envio', 'tiempo', 'logistica', 'demora', 'reparto', 'paquete'],
        language=Language.SPANISH
    ),
    TopicCategory(
        category=BusinessCategory.PRICE,
        keywords=['precio', 'costo', 'valor', 'caro', 'barato', 'economico', 'descuento'],
        language=Language.SPANISH
    )
]

ENGLISH_CATEGORIES = [
    TopicCategory(
        category=BusinessCategory.PRODUCT,
        keywords=['product', 'quality', 'feature', 'design', 'performance', 'material', 'durability'],
        language=Language.ENGLISH
    ),
    TopicCategory(
        category=BusinessCategory.SERVICE,
        keywords=['service', 'support', 'customer', 'help', 'assistance', 'employee', 'staff'],
        language=Language.ENGLISH
    ),
    TopicCategory(
        category=BusinessCategory.DELIVERY,
        keywords=['delivery', 'shipping', 'time', 'logistics', 'delay', 'carrier', 'package'],
        language=Language.ENGLISH
    ),
    TopicCategory(
        category=BusinessCategory.PRICE,
        keywords=['price', 'cost', 'value', 'expensive', 'cheap', 'discount', 'offer'],
        language=Language.ENGLISH
    )
]