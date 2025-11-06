# src/services/topic_service.py - VERSION SIMPLIFICADA
import logging
import re
from typing import List, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class Language(Enum):
    SPANISH = "es"
    ENGLISH = "en"

class TopicService:
    """Servicio de temas - Version simplificada para compatibilidad inmediata"""
    
    def __init__(self):
        self.spanish_categories = {
            'producto': ['producto', 'calidad', 'funcion', 'diseno', 'rendimiento'],
            'servicio': ['servicio', 'atencion', 'soporte', 'asesoramiento', 'trato'],
            'entrega': ['entrega', 'envio', 'tiempo', 'logistica', 'demora'],
            'precio': ['precio', 'costo', 'valor', 'caro', 'barato']
        }
        
        self.english_categories = {
            'product': ['product', 'quality', 'feature', 'design', 'performance'],
            'service': ['service', 'support', 'customer', 'help', 'assistance'],
            'shipping': ['shipping', 'delivery', 'time', 'logistics', 'delay'],
            'price': ['price', 'cost', 'value', 'expensive', 'cheap']
        }
    
    def detect_language(self, text: str) -> Language:
        """Deteccion simple de idioma"""
        text_lower = text.lower()
        spanish_indicators = ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es']
        english_indicators = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on']
        
        spanish_count = sum(1 for word in spanish_indicators if word in text_lower)
        english_count = sum(1 for word in english_indicators if word in text_lower)
        
        return Language.SPANISH if spanish_count > english_count else Language.ENGLISH
    
    def extract_topics_from_legacy(self, legacy_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extraer temas desde resultados legacy - Version simplificada"""
        try:
            topics_by_category = {}
            
            for result in legacy_results:
                text = result.get('text', '').lower()
                sentiment = result.get('sentiment', '3 stars')
                language = self.detect_language(text)
                
                categories = self.spanish_categories if language == Language.SPANISH else self.english_categories
                
                for category, keywords in categories.items():
                    if any(keyword in text for keyword in keywords):
                        if category not in topics_by_category:
                            topics_by_category[category] = {
                                'positive': 0,
                                'negative': 0,
                                'examples': [],
                                'language': language.value
                            }
                        
                        # Contar sentimiento
                        if sentiment in ['4 stars', '5 stars']:
                            topics_by_category[category]['positive'] += 1
                        elif sentiment in ['1 star', '2 stars']:
                            topics_by_category[category]['negative'] += 1
                        
                        # Guardar ejemplo
                        if len(topics_by_category[category]['examples']) < 3:
                            topics_by_category[category]['examples'].append(text[:80] + "...")
            
            # Convertir a formato de salida
            topics = []
            for category, data in topics_by_category.items():
                total = data['positive'] + data['negative']
                if total >= 2:  # Minimo 2 menciones
                    topics.append({
                        'name': category,
                        'category': category,
                        'frequency': total,
                        'negative_ratio': data['negative'] / total if total > 0 else 0,
                        'examples': data['examples'],
                        'language': data['language']
                    })
            
            return sorted(topics, key=lambda x: x['negative_ratio'], reverse=True)
            
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []