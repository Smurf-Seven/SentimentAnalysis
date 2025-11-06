"""Funciones utilitarias para el proyecto"""

import logging
import pandas as pd
import os

def setup_logging():
    """Configura el sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sentiment_analysis.log')
        ]
    )

def load_reviews_data(file_path):
    """Carga datos de reviews desde un archivo CSV"""
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ Datos cargados: {len(df)} reviews")
        return df
    except Exception as e:
        logging.error(f"❌ Error cargando datos: {e}")
        return None

def ensure_directory(path):
    """Asegura que un directorio existe"""
    os.makedirs(path, exist_ok=True)
    return path
