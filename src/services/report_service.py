"""Servicio para generar reportes ejecutivos de análisis"""
"""NO SE USA ACTUAL"""
import pandas as pd
from collections import Counter
from datetime import datetime

class ReportService:
    def __init__(self, sentiment_service):
        self.sentiment_service = sentiment_service
    
    def generate_executive_report(self, df, text_column='review'):
        """Genera reporte ejecutivo para toma de decisiones"""
        
        # 1. Análisis de sentimiento en lote
        texts = df[text_column].tolist()
        results = self.sentiment_service.analyze_batch(texts)
        
        # 2. Métricas clave
        total_reviews = len(results)
        sentiment_dist = self._get_sentiment_distribution(results)
        top_problems = self._get_top_problems(results)
        positive_aspects = self._get_positive_aspects(results)
        
        # 3. Generar reporte
        report = {
            'summary': {
                'total_reviews': total_reviews,
                'average_sentiment': self._calculate_average_sentiment(results),
                'negative_percentage': sentiment_dist.get('1 star', 0) + sentiment_dist.get('2 stars', 0)
            },
            'critical_issues': top_problems[:5],
            'strengths': positive_aspects[:3],
            'recommendations': self._generate_recommendations(top_problems, positive_aspects),
            'timestamp': datetime.now().isoformat()
        }
        
        return report
    
    def _get_sentiment_distribution(self, results):
        """Distribución de sentimientos"""
        sentiments = [r['sentiment'] for r in results]
        return dict(Counter(sentiments))
    
    def _get_top_problems(self, results):
        """Problemas más comunes en reviews negativas"""
        negative_reviews = [r for r in results if r['sentiment'] in ['1 star', '2 stars']]
        
        all_aspects = []
        for review in negative_reviews:
            all_aspects.extend(review.get('aspects', []))
        
        return Counter(all_aspects).most_common(10)
    
    def _generate_recommendations(self, problems, strengths):
        """Genera recomendaciones accionables"""
        recommendations = []
        
        if problems:
            top_problem, freq = problems[0]
            recommendations.append({
                'priority': 'HIGH',
                'action': f'Address issues with {top_problem} ({freq} complaints)',
                'impact': f'Could improve {len(problems)} negative reviews'
            })
        
        if strengths:
            top_strength, freq = strengths[0]
            recommendations.append({
                'priority': 'MEDIUM', 
                'action': f'Leverage strength in {top_strength} in marketing',
                'impact': f'Highlighted in {freq} positive reviews'
            })
        
        return recommendations