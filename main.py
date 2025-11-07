# main.py (debería estar en la raíz)
#!/usr/bin/env python3
"""Sistema de ANALISIS de Sentimiento - Arquitectura Mejorada"""

import sys
import os

# Configurar paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.sentiment_service import SentimentService

def main():
    print("🚀 SISTEMA DE ANALISIS - ARQUITECTURA MEJORADA")
    print("=" * 50)
    
    try:
        # Inicializar servicio
        service = SentimentService()
        print(f"✅ Modelos disponibles: {service.get_available_models()}")
        
        # Mostrar info de cada modelo
        for model_name in service.get_available_models():
            info = service.get_model_info(model_name)
            print(f"   📊 {model_name}: {info}")

        
        # Probar ANALISIS
        test_texts = [
            "I love this product! It's amazing!",
            "This is terrible and I hate it.",
            "It's okay, nothing special.",
            "The customer service was excellent and very helpful.",
            "Poor quality, broke after one week of use."
        ]
        
        print("\n🧪 PRUEBAS DE ANALISIS:")
        print("-" * 40)
        
        for text in test_texts:
            result = service.analyze_text(text)
            print(f"📝 '{text}'")
            print(f"   → Sentimiento: {result['sentiment']}")
            print(f"   → Confianza: {result['confidence']:.2f}")
            print(f"   → Modelo: {result['model_used']}")
            print()
        
        print("🎯 ¡SISTEMA FUNCIONANDO CORRECTAMENTE!")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()