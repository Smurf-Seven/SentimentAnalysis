# src/services/topic_service.py - SOLO COORDINACIÓN
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TopicService:
    """Servicio de temas - SOLO coordina, CERO LOGICA de negocio"""
    
    def __init__(self):
        # ✅ DELEGA toda la LOGICA de negocio al core
        self.multi_language_extractor = self._initialize_extractor()
    
    def _initialize_extractor(self):
        """Inicializar el extractor multiidioma - SOLO COORDINACIÓN"""
        try:
            from core.topic_extraction.multi_language import MultiLanguageTopicExtractor
            return MultiLanguageTopicExtractor()
        except ImportError as e:
            logger.warning(f"MultiLanguage extractor not available: {e}")
            return None
    
    def extract_topics_from_legacy(self, legacy_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extraer temas desde resultados legacy
        RESPONSABILIDAD: Solo coordinar el proceso
        """
        if not self.multi_language_extractor:
            logger.warning("Topic extractor not available")
            return []
        
        try:
            # 1. CONVERSIÓN de formatos (responsabilidad del servicio)
            analyzed_texts = self._convert_to_domain_entities(legacy_results)
            
            # 2. ✅ DELEGACIÓN a core (ellos tienen la LOGICA de negocio)
            domain_topics = self.multi_language_extractor.extract(analyzed_texts)
            
            # 3. CONVERSIÓN a formato legacy
            return self._convert_to_legacy_format(domain_topics)
            
        except Exception as e:
            logger.error(f"Error in topic extraction coordination: {e}")
            return []
    
    def _convert_to_domain_entities(self, legacy_results: List[Dict[str, Any]]) -> List[Any]:
        """Convertir resultados legacy a entidades de dominio - RESPONSABILIDAD DEL SERVICIO"""
        try:
            from domain.entities import AnalyzedText
            return [AnalyzedText.from_legacy(result) for result in legacy_results]
        except ImportError as e:
            logger.error(f"Error importing domain entities: {e}")
            return []
    
    def _convert_to_legacy_format(self, domain_topics: List[Any]) -> List[Dict[str, Any]]:
        """Convertir temas de dominio a formato legacy - RESPONSABILIDAD DEL SERVICIO"""
        try:
            if hasattr(domain_topics[0], 'to_legacy_dict'):
                return [topic.to_legacy_dict() for topic in domain_topics]
            else:
                # Fallback si no tiene el método
                return []
        except (IndexError, AttributeError):
            return []