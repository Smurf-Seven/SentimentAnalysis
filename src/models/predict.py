"""Predicciones de sentiment analysis - Versión compatible Windows"""

import logging
import re
from collections import Counter
import sys

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.model = None
        self.use_transformers = False
        self.load_model()
    
    def load_model(self):
        """Intenta cargar el mejor modelo disponible"""
        # Primero intentar con transformers (BERT)
        try:
            from transformers import pipeline
            logger.info("Cargando modelo BERT...")
            self.model = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment"
            )
            self.use_transformers = True
            logger.info("Modelo BERT cargado correctamente")
            return
        except ImportError:
            logger.warning("Transformers no disponible")
        except Exception as e:
            logger.warning(f"BERT no disponible: {e}")
        
        # Fallback a TextBlob
        try:
            from textblob import TextBlob
            logger.info("Usando TextBlob como fallback...")
            self.model = "textblob"
            logger.info("TextBlob configurado")
            return
        except ImportError:
            logger.error("TextBlob tampoco disponible")
        
        # Último fallback - análisis muy basico
        logger.warning("Usando analisis basico por palabras clave")
        self.model = "basic"
    
    def analyze_with_bert(self, text):
        """Análisis usando transformers/BERT"""
        try:
            result = self.model(text[:512])[0]
            return result['label'], result['score']
        except Exception as e:
            logger.error(f"Error con BERT: {e}")
            return "NEUTRAL", 0.5
    
    def analyze_with_textblob(self, text):
        """Análisis usando TextBlob"""
        try:
            from textblob import TextBlob
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return "POSITIVE", abs(polarity)
            elif polarity < -0.1:
                return "NEGATIVE", abs(polarity)
            else:
                return "NEUTRAL", abs(polarity)
        except Exception as e:
            logger.error(f"Error con TextBlob: {e}")
            return "NEUTRAL", 0.5
    
    def analyze_with_basic(self, text):
        """Análisis basico por palabras clave"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'awesome', 'perfect', 'nice', 'best', 'fantastic']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible', 'disappointing', 'poor', 'waste', 'rubbish']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "POSITIVE", min(0.9, positive_count * 0.2)
        elif negative_count > positive_count:
            return "NEGATIVE", min(0.9, negative_count * 0.2)
        else:
            return "NEUTRAL", 0.5
    
    def extract_aspects_simple(self, text):
        """Extrae aspectos simples usando regex"""
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'}
        
        # Encontrar palabras sustantivas (patrón simple)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        aspects = [word for word in words if word not in stop_words and len(word) > 2]
        
        return aspects
    
    def analyze_text(self, text):
        """Analiza el sentimiento usando el mejor método disponible"""
        if not self.model:
            sentiment, confidence = "NEUTRAL", 0.5
        elif self.use_transformers:
            sentiment, confidence = self.analyze_with_bert(text)
        elif self.model == "textblob":
            sentiment, confidence = self.analyze_with_textblob(text)
        else:
            sentiment, confidence = self.analyze_with_basic(text)
        
        return {
            'text': text,
            'sentiment': sentiment,
            'confidence': confidence,
            'aspects': self.extract_aspects_simple(text),
            'method': 'BERT' if self.use_transformers else 'TextBlob' if self.model == "textblob" else 'Basic'
        }
    
    def analyze_batch(self, texts):
        """Analiza una lista de textos"""
        logger.info(f"Analizando {len(texts)} textos con {self.model}...")
        results = []
        
        for i, text in enumerate(texts):
            if i % 20 == 0 and i > 0:
                logger.info(f"Procesado {i}/{len(texts)} textos...")
            
            result = self.analyze_text(text)
            results.append(result)
        
        logger.info(f"Analisis completado: {len(results)} textos")
        return results
