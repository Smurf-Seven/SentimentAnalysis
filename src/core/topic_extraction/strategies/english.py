from .spanish import SpanishTopicExtractor
from domain.entities import Language

class EnglishTopicExtractor(SpanishTopicExtractor):
    """Extracción de temas para inglés - hereda estructura pero cambia categorías"""
    
    @property
    def supported_language(self) -> Language:
        return Language.ENGLISH
    
    def __init__(self):
        super().__init__()
        self.categories = {
            'product': {
                'keywords': ['product', 'quality', 'feature', 'design', 'performance',
                           'functionality', 'material', 'durability'],
                'phrases': ['product quality', 'product design']
            },
            'service': {
                'keywords': ['service', 'support', 'customer', 'help', 'assistance',
                           'employee', 'staff', 'advisor'],
                'phrases': ['customer service', 'customer support']
            },
            'shipping': {
                'keywords': ['shipping', 'delivery', 'time', 'logistics', 'delay',
                           'carrier', 'package', 'shipment'],
                'phrases': ['delivery time', 'shipping cost']
            },
            'price': {
                'keywords': ['price', 'cost', 'value', 'expensive', 'cheap',
                           'discount', 'offer', 'spend'],
                'phrases': ['value for money', 'fair price']
            }
        }
        
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
        }