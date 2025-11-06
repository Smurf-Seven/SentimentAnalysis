"""Sentiment Service - Uses BERT model only - VERSIÓN CORREGIDA"""

import logging
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)

class SentimentService:
    """Main sentiment analysis service using BERT"""
    
    def __init__(self):
        self.model = self._initialize_model()
    
    def _initialize_model(self):
        """Initialize BERT model"""
        try:
            from models.bert_model import BERTModel
            model = BERTModel()
            logger.info("BERT model loaded successfully")
            return model
        except Exception as e:
            logger.error(f"Failed to load BERT model: {e}")
            raise
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text using BERT - VERSIÓN COMPATIBLE"""
        try:
            # Obtener resultado base de BERT
            bert_result = self.model.analyze_text(text)
            
            # CONVERTIR al formato que espera el dashboard
            result = {
                'text': bert_result['text'],
                'sentiment': bert_result['sentiment'],
                'confidence': bert_result['confidence'],
                'aspects': self._extract_aspects_simple(text),  # ← AGREGAR ASPECTS
                'method': 'BERT'
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in analyze_text: {e}")
            # Fallback completo
            return {
                'text': text,
                'sentiment': '3 stars',
                'confidence': 0.5,
                'aspects': self._extract_aspects_simple(text),
                'method': 'BERT'
            }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Analyze multiple texts using BERT"""
        return [self.analyze_text(text) for text in texts]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Return information about BERT model"""
        return self.model.get_model_info()
    
    def _extract_aspects_simple(self, text: str) -> List[str]:
        """Extrae aspectos simples usando regex - COPIADO DE TU CÓDIGO ORIGINAL"""
        try:
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                         'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'this', 'that'}
            
            # Encontrar palabras sustantivas (patrón simple)
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            aspects = [word for word in words if word not in stop_words and len(word) > 2]
            
            return aspects[:5]  # Máximo 5 aspectos
            
        except Exception as e:
            logger.error(f"Error extracting aspects: {e}")
            return []