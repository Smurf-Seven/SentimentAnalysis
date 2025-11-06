"""Clase base para todos los modelos de sentiment analysis"""

from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseSentimentModel(ABC):
    """Interfaz que todos los modelos deben implementar"""
    
    @abstractmethod
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analiza el sentimiento de un texto"""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informacion sobre el modelo"""
        pass
    
    def analyze_batch(self, texts: list) -> list:
        """Analiza multiples textos (implementacion por defecto)"""
        return [self.analyze_text(text) for text in texts]