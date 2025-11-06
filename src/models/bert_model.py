"""BERT Model for sentiment analysis"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class BERTModel:
    """BERT-based sentiment analysis model"""
    
    def __init__(self):
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load BERT model"""
        try:
            from transformers import pipeline
            logger.info("Loading BERT model...")
            self.model = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                truncation=True
            )
            logger.info("BERT model loaded successfully")
        except ImportError:
            logger.error("Transformers not available")
            raise
        except Exception as e:
            logger.error(f"Error loading BERT: {e}")
            raise
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment using BERT"""
        try:
            result = self.model(text[:512])[0]
            return {
                'text': text,
                'sentiment': result['label'],
                'confidence': result['score'],
                'model': 'BERT',
                'success': True
            }
        except Exception as e:
            logger.error(f"Error analyzing with BERT: {e}")
            return {
                'text': text,
                'sentiment': 'NEUTRAL',
                'confidence': 0.0,
                'model': 'BERT',
                'success': False,
                'error': str(e)
            }
    
    def get_model_info(self) -> Dict[str, Any]:
        return {
            'name': 'BERT',
            'provider': 'Hugging Face',
            'type': 'Transformer',
            'status': 'loaded' if self.model else 'error'
        }