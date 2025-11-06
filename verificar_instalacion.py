#!/usr/bin/env python3
"""
Script de instalación automática de dependencias
"""

import subprocess
import sys
import time

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n📦 {descripcion}...")
    print(f"   Comando: {comando}")
    
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"   ✅ {descripcion} - EXITOSO")
            return True
        else:
            print(f"   ❌ {descripcion} - FALLÓ")
            print(f"      Error: {resultado.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ {descripcion} - EXCEPCIÓN: {e}")
        return False

def main():
    print("🚀 INSTALADOR AUTOMÁTICO DE DEPENDENCIAS")
    print("=" * 50)
    
    comandos = [
        (
            [sys.executable, "-m", "pip", "install", "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn", "jupyter"],
            "Instalando paquetes base"
        ),
        (
            [sys.executable, "-m", "pip", "install", "torch", "torchvision", "torchaudio", "--index-url", "https://download.pytorch.org/whl/cpu"],
            "Instalando PyTorch (CPU)"
        ),
        (
            [sys.executable, "-m", "pip", "install", "transformers"],
            "Instalando Transformers"
        ),
        (
            [sys.executable, "-m", "pip", "install", "spacy", "textblob", "nltk"],
            "Instalando procesamiento de texto"
        ),
        (
            [sys.executable, "-m", "pip", "install", "streamlit", "plotly", "wordcloud"],
            "Instalando visualización"
        ),
    ]
    
    exitosos = 0
    for comando, descripcion in comandos:
        # Convertir lista a string para shell
        comando_str = " ".join(comando)
        if ejecutar_comando(comando_str, descripcion):
            exitosos += 1
        time.sleep(1)  # Pequeña pausa entre instalaciones
    
    print(f"\n📊 RESUMEN: {exitosos}/{len(comandos)} instalaciones exitosas")
    
    if exitosos == len(comandos):
        print("🎉 ¡TODAS LAS DEPENDENCIAS INSTALADAS!")
        print("\n🔧 Instalando modelo de spaCy...")
        subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    else:
        print("⚠️  Algunas instalaciones fallaron, revisa los errores")

if __name__ == "__main__":
    main()