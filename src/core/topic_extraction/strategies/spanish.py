import re
from typing import List, Dict
from domain.entities import AnalyzedText, Topic, Language, SentimentLabel
from .base import BaseTopicExtractor

class SpanishTopicExtractor(BaseTopicExtractor):
    """Extracción de temas para español"""
    
    @property
    def supported_language(self) -> Language:
        return Language.SPANISH
    
    def __init__(self):
        self.categories = {
            'producto': {
                'keywords': ['producto', 'calidad', 'funcion', 'diseño', 'rendimiento', 
                           'característica', 'material', 'durabilidad'],
                'phrases': ['calidad del producto', 'diseño del producto']
            },
            'servicio': {
                'keywords': ['servicio', 'atención', 'soporte', 'asesoramiento', 'trato',
                           'empleado', 'vendedor', 'asesor'],
                'phrases': ['atención al cliente', 'servicio al cliente']
            },
            'entrega': {
                'keywords': ['entrega', 'envío', 'tiempo', 'logística', 'demora',
                           'reparto', 'transportista', 'paquete'],
                'phrases': ['tiempo de entrega', 'costo de envío']
            },
            'precio': {
                'keywords': ['precio', 'costo', 'valor', 'caro', 'barato', 'económico',
                           'descuento', 'oferta', 'gasto'],
                'phrases': ['relación calidad-precio', 'precio justo']
            }
        }
        
        self.stop_words = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'pero',
            'en', 'a', 'de', 'con', 'por', 'para', 'sin', 'sobre', 'entre', 'hacia'
        }
    
    def extract(self, texts: List[AnalyzedText]) -> List[Topic]:
        topics_by_category = {}
        
        for text in texts:
            text_lower = text.text.lower()
            
            for category, config in self.categories.items():
                # Buscar frases primero (más específico)
                phrase_matches = self._find_phrases(text_lower, config['phrases'])
                keyword_matches = self._find_keywords(text_lower, config['keywords'])
                
                if phrase_matches or keyword_matches:
                    if category not in topics_by_category:
                        topics_by_category[category] = []
                    topics_by_category[category].append(text)
        
        # Convertir a objetos Topic
        return self._build_topics(topics_by_category)
    
    def _find_phrases(self, text: str, phrases: List[str]) -> List[str]:
        """Encontrar frases específicas en el texto"""
        found = []
        for phrase in phrases:
            if phrase in text:
                found.append(phrase)
        return found
    
    def _find_keywords(self, text: str, keywords: List[str]) -> List[str]:
        """Encontrar palabras clave en el texto"""
        words = set(re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', text))
        return [kw for kw in keywords if kw in words]
    
    def _build_topics(self, topics_by_category: Dict[str, List[AnalyzedText]]) -> List[Topic]:
        """Construir objetos Topic a partir de los textos agrupados"""
        topics = []
        
        for category, texts in topics_by_category.items():
            if len(texts) >= 2:  # Mínimo 2 menciones para considerar tema
                sentiment_dist = self._calculate_sentiment_distribution(texts)
                examples = [t.text[:100] + "..." for t in texts[:3]]
                
                topic = Topic(
                    name=category,
                    category=category,
                    frequency=len(texts),
                    sentiment_distribution=sentiment_dist,
                    examples=examples,
                    language=self.supported_language
                )
                topics.append(topic)
        
        return topics