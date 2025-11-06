import streamlit as st
import pandas as pd
import sys
import os
from collections import Counter
import plotly.express as px
import re

# ========== CONFIGURACIÓN DE PATHS ==========
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, os.path.join(project_root, 'src', 'services'))
sys.path.insert(0, os.path.join(project_root, 'src', 'models'))

try:
    from sentiment_service import SentimentService
    from dataset_analyzer import DatasetAnalyzer
    st.success("✅ Sistema de análisis cargado correctamente")
except ImportError as e:
    st.error(f"❌ Error cargando el sistema: {e}")
    st.stop()

def extract_aspects_simple(text):
    """Extraer palabras clave simples del texto - EN EL FRONTEND"""
    if not text or not isinstance(text, str):
        return []
    
    try:
        # Palabras comunes a excluir
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 
                     'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'this', 
                     'that', 'with', 'have', 'has', 'had', 'been', 'being', 'do',
                     'does', 'did', 'will', 'would', 'could', 'should', 'may',
                     'might', 'must', 'can', 'its', 'their', 'what', 'which',
                     'who', 'whom', 'whose', 'where', 'when', 'why', 'how'}
        
        # Limpiar y extraer palabras
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        aspects = [word for word in words if word not in stop_words and len(word) > 2]
        
        return aspects[:5]  # Máximo 5 aspectos
        
    except Exception:
        return []

def main():
    st.set_page_config(
        page_title="Analizador de Sentimientos", 
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 Sistema de Análisis de Clientes")
    st.markdown("**Sube tus datos y obtén insights automáticos en minutos**")
    st.markdown("---")
    
    # Inicializar servicios
    @st.cache_resource
    def load_services():
        sentiment_service = SentimentService()
        analyzer = DatasetAnalyzer(sentiment_service)
        return sentiment_service, analyzer
    
    sentiment_service, analyzer = load_services()
    
    # SECCIÓN: SUBIDA DE ARCHIVOS
    st.header("📤 Subir Datos")
    uploaded_file = st.file_uploader(
        "Arrastra tu archivo CSV o Excel aquí", 
        type=['csv', 'xlsx'],
        help="Formatos soportados: CSV, Excel"
    )
    
    if uploaded_file:
        # Cargar datos
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.success(f"✅ **Datos cargados:** {len(df)} filas, {len(df.columns)} columnas")
            
            # SECCIÓN: DETECCIÓN DE COLUMNAS
            st.header("🔍 Configuración del Análisis")
            
            # Detectar columnas de texto automáticamente
            text_columns = []
            for col in df.columns:
                col_lower = col.lower()
                if any(keyword in col_lower for keyword in ['text', 'comment', 'review', 'tweet', 'message', 'content', 'clean_']):
                    text_columns.append(col)
                elif df[col].dtype == 'object' and df[col].astype(str).str.len().mean() > 10:
                    text_columns.append(col)
            
            if text_columns:
                text_column = st.selectbox(
                    "**Selecciona la columna que contiene el texto a analizar:**",
                    text_columns,
                    index=0,
                    help="Esta columna debe contener los comentarios, reviews o textos a analizar"
                )
            else:
                st.warning("⚠️ No se detectaron columnas de texto automáticamente")
                text_column = st.selectbox(
                    "**Selecciona manualmente la columna de texto:**",
                    df.columns,
                    help="Selecciona la columna que contiene los textos a analizar"
                )
            
            # Vista previa de datos
            with st.expander("📊 **Vista previa de los datos (primeras 10 filas)**", expanded=False):
                st.dataframe(df.head(10), use_container_width=True)
                st.write(f"**Columnas disponibles:** {list(df.columns)}")
            
            # SECCIÓN: ANÁLISIS
            st.header("🎯 Ejecutar Análisis")
            
            sample_size = st.slider(
                "**Número de muestras a analizar:**",
                min_value=50,
                max_value=min(1000, len(df)),
                value=min(300, len(df)),
                help="Para datasets grandes, analizar una muestra es más rápido"
            )
            
            if st.button("🚀 **Ejecutar Análisis Completo**", type="primary", use_container_width=True):
                with st.spinner(f"🔍 Analizando {sample_size} textos con BERT..."):
                    # Preparar datos
                    df_sample = df.sample(sample_size, random_state=42)
                    texts = df_sample[text_column].dropna().tolist()
                    
                    if not texts:
                        st.error("❌ No hay textos válidos para analizar")
                        return
                    
                    # Análisis de sentimientos
                    results = sentiment_service.analyze_batch(texts)
                    
                    # SECCIÓN: RESULTADOS
                    st.header("📈 Resultados del Análisis")
                    
                    # Métricas principales
                    st.subheader("📊 Métricas Clave")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    # Calcular métricas
                    sentiments = [r['sentiment'] for r in results]
                    sentiment_counts = Counter(sentiments)
                    
                    total = len(results)
                    positive = sum(1 for s in sentiments if '4 stars' in s or '5 stars' in s)
                    negative = sum(1 for s in sentiments if '1 star' in s or '2 stars' in s)
                    neutral = total - positive - negative
                    
                    with col1:
                        st.metric("👍 Positivos", f"{(positive/total)*100:.1f}%", f"{positive} textos")
                    
                    with col2:
                        st.metric("👎 Negativos", f"{(negative/total)*100:.1f}%", f"{negative} textos")
                    
                    with col3:
                        st.metric("⚖️ Neutrales", f"{(neutral/total)*100:.1f}%", f"{neutral} textos")
                    
                    with col4:
                        avg_rating = sum(
                            5 if '5 stars' in s else
                            4 if '4 stars' in s else  
                            3 if '3 stars' in s else
                            2 if '2 stars' in s else 1 
                            for s in sentiments
                        ) / total
                        st.metric("⭐ Rating Promedio", f"{avg_rating:.1f}/5")
                    
                    # Gráfico de distribución
                    st.subheader("📊 Distribución de Sentimientos")
                    
                    # Preparar datos para el gráfico
                    sentiment_df = pd.DataFrame({
                        'Sentimiento': list(sentiment_counts.keys()),
                        'Cantidad': list(sentiment_counts.values())
                    })
                    
                    fig = px.bar(
                        sentiment_df, 
                        x='Sentimiento', 
                        y='Cantidad',
                        color='Sentimiento',
                        title="Distribución de Sentimientos por Estrellas"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # PROBLEMAS CRÍTICOS
                    st.subheader("🚨 Problemas Críticos Detectados")
                    
                    if negative > 0:
                        negative_reviews = [r for r in results if '1 star' in r['sentiment'] or '2 stars' in r['sentiment']]
                        all_aspects = []
                        
                        for review in negative_reviews:
                            # EXTRAER ASPECTOS EN EL FRONTEND
                            aspects = extract_aspects_simple(review['text'])
                            all_aspects.extend(aspects)
                        
                        top_issues = Counter(all_aspects).most_common(8)
                        
                        if top_issues:
                            st.info("**Temas más mencionados en reviews negativos:**")
                            for issue, count in top_issues:
                                st.write(f"• **{issue}** - mencionado en {count} quejas")
                        else:
                            st.warning("No se detectaron aspectos específicos en las reviews negativas")
                    else:
                        st.success("🎉 **Excelente!** No se detectaron reviews negativas en la muestra analizada")
                    
                    # FORTALEZAS
                    st.subheader("💪 Fortalezas Detectadas")
                    
                    if positive > 0:
                        positive_reviews = [r for r in results if '4 stars' in r['sentiment'] or '5 stars' in r['sentiment']]
                        positive_aspects = []
                        
                        for review in positive_reviews:
                            # EXTRAER ASPECTOS EN EL FRONTEND
                            aspects = extract_aspects_simple(review['text'])
                            positive_aspects.extend(aspects)
                        
                        top_strengths = Counter(positive_aspects).most_common(5)
                        
                        if top_strengths:
                            st.info("**Temas más mencionados en reviews positivos:**")
                            for strength, count in top_strengths:
                                st.write(f"• **{strength}** - mencionado en {count} elogios")
                    
                    # EJEMPLOS DETALLADOS
                    st.subheader("📝 Ejemplos de Análisis")
                    
                    tab1, tab2, tab3 = st.tabs(["👍 Positivos", "👎 Negativos", "⚖️ Neutrales"])
                    
                    with tab1:
                        positive_examples = [r for r in results if '4 stars' in r['sentiment'] or '5 stars' in r['sentiment']][:5]
                        for i, example in enumerate(positive_examples, 1):
                            with st.expander(f"Ejemplo positivo {i}: {example['sentiment']} (confianza: {example.get('confidence', 0):.2f})"):
                                st.write(f"**Texto:** {example['text']}")
                                aspects = extract_aspects_simple(example['text'])
                                if aspects:
                                    st.write(f"**Palabras clave:** {', '.join(aspects)}")
                    
                    with tab2:
                        negative_examples = [r for r in results if '1 star' in r['sentiment'] or '2 stars' in r['sentiment']][:5]
                        for i, example in enumerate(negative_examples, 1):
                            with st.expander(f"Ejemplo negativo {i}: {example['sentiment']} (confianza: {example.get('confidence', 0):.2f})"):
                                st.write(f"**Texto:** {example['text']}")
                                aspects = extract_aspects_simple(example['text'])
                                if aspects:
                                    st.write(f"**Palabras clave:** {', '.join(aspects)}")
                    
                    with tab3:
                        neutral_examples = [r for r in results if '3 stars' in r['sentiment']][:5]
                        for i, example in enumerate(neutral_examples, 1):
                            with st.expander(f"Ejemplo neutral {i}: {example['sentiment']} (confianza: {example.get('confidence', 0):.2f})"):
                                st.write(f"**Texto:** {example['text']}")
                                aspects = extract_aspects_simple(example['text'])
                                if aspects:
                                    st.write(f"**Palabras clave:** {', '.join(aspects)}")
                    
                    # RECOMENDACIONES
                    st.subheader("💡 Recomendaciones Accionables")
                    
                    if negative > 0:
                        negative_reviews = [r for r in results if '1 star' in r['sentiment'] or '2 stars' in r['sentiment']]
                        all_negative_aspects = []
                        for review in negative_reviews:
                            aspects = extract_aspects_simple(review['text'])
                            all_negative_aspects.extend(aspects)
                        
                        if all_negative_aspects:
                            top_issue, count = Counter(all_negative_aspects).most_common(1)[0]
                            st.warning(f"**Prioridad ALTA:** Abordar problemas relacionados con **{top_issue}**")
                            st.write(f"*Impacto potencial: Este tema aparece en {count} de {len(negative_reviews)} reviews negativas*")
                    
                    if positive > 0:
                        positive_reviews = [r for r in results if '4 stars' in r['sentiment'] or '5 stars' in r['sentiment']]
                        all_positive_aspects = []
                        for review in positive_reviews:
                            aspects = extract_aspects_simple(review['text'])
                            all_positive_aspects.extend(aspects)
                        
                        if all_positive_aspects:
                            top_strength, count = Counter(all_positive_aspects).most_common(1)[0]
                            st.success(f"**Oportunidad:** Potenciar **{top_strength}** en estrategias de marketing")
                            st.write(f"*Este aspecto es mencionado en {count} reviews positivas*")
                        
        except Exception as e:
            st.error(f"❌ Error procesando el archivo: {e}")
            st.info("💡 **Sugerencia:** Verifica que el archivo esté en formato correcto y no esté corrupto")

if __name__ == "__main__":
    main()