"""Analyze datasets using BERT model"""

import pandas as pd
import os
from collections import Counter
from typing import Dict, Any

class DatasetAnalyzer:
    """Analyze sentiment datasets using BERT"""
    
    def __init__(self, sentiment_service):
        self.sentiment_service = sentiment_service
    
    def analyze_dataset_comparison(self, file_path: str, sample_size: int = 100):
        """Analyze dataset and compare with BERT"""
        print(f"Loading dataset: {file_path}")
        
        try:
            df = pd.read_csv(file_path)
            print(f"Dataset: {len(df)} records")
            
            # Sample for analysis
            df_sample = df.sample(min(sample_size, len(df)), random_state=42)
            
            # Get text column
            text_column = self._find_text_column(df_sample)
            if not text_column:
                return None
            
            # Analyze with BERT
            our_results = self._analyze_with_bert(df_sample, text_column)
            
            # Compare approaches
            return self._compare_approaches(df_sample, our_results, text_column)
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _analyze_with_bert(self, df, text_column):
        """Analyze with BERT keeping original 1-5 star scale"""
        texts = df[text_column].dropna().tolist()
        return self.sentiment_service.analyze_batch(texts)
    
    def _compare_approaches(self, df, our_results, text_column):
        """Compare BERT with dataset labels"""
        print("\n=== BERT vs DATASET COMPARISON ===")
        
        # BERT distribution (1-5 stars)
        our_sentiments = [r['sentiment'] for r in our_results]
        our_dist = Counter(our_sentiments)
        
        print("BERT SENTIMENT (1-5 stars):")
        for sentiment, count in our_dist.most_common():
            percentage = (count / len(our_results)) * 100
            print(f"  {sentiment}: {count} ({percentage:.1f}%)")
        
        # Dataset distribution (0-2)
        if 'Sentiment' in df.columns:
            true_dist = Counter(df['Sentiment'])
            print("\nDATASET LABELS (0-2 scale):")
            label_names = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}
            for sentiment, count in true_dist.most_common():
                percentage = (count / len(df)) * 100
                name = label_names.get(sentiment, f"Label_{sentiment}")
                print(f"  {name} ({sentiment}): {count} ({percentage:.1f}%)")
        
        # Show examples
        print("\n=== EXAMPLE COMPARISONS ===")
        print("Format: Text -> BERT | Dataset_Label")
        
        for i in range(min(5, len(our_results))):
            our_sentiment = our_results[i]['sentiment']
            true_label = df['Sentiment'].iloc[i] if 'Sentiment' in df.columns else 'N/A'
            true_label_name = {0: 'Negative', 1: 'Neutral', 2: 'Positive'}.get(true_label, true_label)
            
            text_preview = df[text_column].iloc[i][:60] + "..." if len(df[text_column].iloc[i]) > 60 else df[text_column].iloc[i]
            
            print(f"\n'{text_preview}'")
            print(f"  → BERT: {our_sentiment} | Dataset: {true_label_name} ({true_label})")
        
        return {
            'bert_distribution': dict(our_dist),
            'dataset_distribution': dict(true_dist) if 'Sentiment' in df.columns else {},
            'sample_size': len(our_results)
        }
    
    def _find_text_column(self, df):
        """Find text column in dataframe"""
        for col in ['clean_text', 'Comment', 'comment', 'text', 'review', 'Tweet']:
            if col in df.columns:
                return col
        return None

    def generate_insights_report(self, file_path: str, sample_size: int = 500):
        """Generate business insights using BERT"""
        print(f"\n=== BERT BUSINESS INSIGHTS ===")
        
        df = pd.read_csv(file_path)
        df_sample = df.sample(min(sample_size, len(df)), random_state=42)
        
        text_column = self._find_text_column(df_sample)
        if not text_column:
            return None
        
        # Analyze with BERT
        our_results = self._analyze_with_bert(df_sample, text_column)
        
        # Generate insights based on BERT's 1-5 star system
        insights = self._generate_business_insights(our_results)
        
        print("📊 BERT BUSINESS INSIGHTS:")
        print(f"  • Average rating: {insights['average_rating']:.1f}/5 stars")
        print(f"  • Positive reviews (4-5 stars): {insights['positive_percentage']:.1f}%")
        print(f"  • Negative reviews (1-2 stars): {insights['negative_percentage']:.1f}%")
        
        if insights['common_issues']:
            print(f"  • Top issues: {', '.join([issue for issue, _ in insights['common_issues'][:3]])}")
        
        return insights
    
    def _generate_business_insights(self, results):
        """Generate insights using BERT's 1-5 star scale"""
        # Map star ratings to counts
        star_counts = Counter()
        for result in results:
            sentiment = result['sentiment']
            if '5 stars' in sentiment:
                star_counts[5] += 1
            elif '4 stars' in sentiment:
                star_counts[4] += 1
            elif '3 stars' in sentiment:
                star_counts[3] += 1
            elif '2 stars' in sentiment:
                star_counts[2] += 1
            elif '1 star' in sentiment:
                star_counts[1] += 1
        
        # Calculate metrics
        total = sum(star_counts.values())
        average_rating = sum(star * count for star, count in star_counts.items()) / total if total > 0 else 0
        
        positive_reviews = star_counts[4] + star_counts[5]
        negative_reviews = star_counts[1] + star_counts[2]
        
        # Get common aspects from negative reviews
        common_issues = []
        for result in results:
            if any(star in result['sentiment'] for star in ['1 star', '2 stars']):
                common_issues.extend(result.get('aspects', []))
        
        return {
            'average_rating': average_rating,
            'positive_percentage': (positive_reviews / total) * 100,
            'negative_percentage': (negative_reviews / total) * 100,
            'star_distribution': dict(star_counts),
            'common_issues': Counter(common_issues).most_common(5)
        }

    """eliminar lo sgte, solo para test de reddit"""
    def analyze_reddit_dataset(self, file_path: str, sample_size: int = 100):
        """Analyze Reddit dataset with -1,0,1 labels"""
        print(f"Loading Reddit dataset: {file_path}")
    
        try:
            df = pd.read_csv(file_path)
            print(f"Reddit dataset: {len(df)} records")
            print(f"Columns: {list(df.columns)}")
        
            # Show dataset structure
            print(f"First rows:")
            print(df.head())
        
            # Sample for analysis
            df_sample = df.sample(min(sample_size, len(df)), random_state=42)
        
            # Find text column (different names in this dataset)
            text_column = None
            for col in ['clean_comment', 'clean_text', 'comment', 'text', 'tweet']:
                if col in df.columns:
                    text_column = col
                    break
        
            if not text_column:
                print("No text column found")
                return None
        
            # Analyze with BERT
            our_results = self._analyze_with_bert(df_sample, text_column)
        
            # Compare with Reddit's -1,0,1 scale
            return self._compare_with_reddit_labels(df_sample, our_results, text_column)
        
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _compare_with_reddit_labels(self, df, our_results, text_column):
        """Compare BERT with Reddit's -1,0,1 labels"""
        print("\n=== BERT vs REDDIT COMPARISON ===")
    
        # BERT distribution (1-5 stars)
        our_sentiments = [r['sentiment'] for r in our_results]
        our_dist = Counter(our_sentiments)
    
        print("BERT SENTIMENT (1-5 stars):")
        for sentiment, count in our_dist.most_common():
            percentage = (count / len(our_results)) * 100
            print(f"  {sentiment}: {count} ({percentage:.1f}%)")
    
        # Reddit distribution (-1,0,1)
        if 'category' in df.columns:
            true_dist = Counter(df['category'])
            print("\nREDDIT LABELS (-1,0,1 scale):")
            label_names = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}
            for sentiment, count in true_dist.most_common():
                percentage = (count / len(df)) * 100
                name = label_names.get(sentiment, f"Label_{sentiment}")
                print(f"  {name} ({sentiment}): {count} ({percentage:.1f}%)")
    
        # Map BERT to Reddit scale for comparison
        print("\n=== MAPPED COMPARISON ===")
        print("Mapping: 4-5 stars → Positive(1), 3 stars → Neutral(0), 1-2 stars → Negative(-1)")
    
        def map_bert_to_reddit(bert_sentiment):
            if '5 stars' in bert_sentiment or '4 stars' in bert_sentiment:
                return 1  # Positive
            elif '3 stars' in bert_sentiment:
                return 0  # Neutral
            elif '1 star' in bert_sentiment or '2 stars' in bert_sentiment:
                return -1  # Negative
            else:
                return 0  # Default to neutral
    
        our_mapped = [map_bert_to_reddit(r['sentiment']) for r in our_results]
        true_labels = df['category'].values if 'category' in df.columns else []
    
        if len(true_labels) > 0:
            # Calculate accuracy with mapped values
            correct = sum(1 for i in range(len(our_mapped)) 
                         if our_mapped[i] == true_labels[i])
            accuracy = correct / len(our_mapped)
        
            print(f"Accuracy (mapped to -1,0,1): {accuracy:.2%}")
            print(f"Correct: {correct}/{len(our_mapped)}")
    
        # Show examples
        print("\n=== EXAMPLE COMPARISONS ===")
        print("Format: Text -> BERT | Reddit_Label")
    
        for i in range(min(5, len(our_results))):
            our_sentiment = our_results[i]['sentiment']
            true_label = df['category'].iloc[i] if 'category' in df.columns else 'N/A'
            true_label_name = {-1: 'Negative', 0: 'Neutral', 1: 'Positive'}.get(true_label, true_label)
        
            text_preview = df[text_column].iloc[i][:60] + "..." if len(df[text_column].iloc[i]) > 60 else df[text_column].iloc[i]
        
            print(f"\n'{text_preview}'")
            print(f"  → BERT: {our_sentiment} | Reddit: {true_label_name} ({true_label})")
    
        return {
            'bert_distribution': dict(our_dist),
            'reddit_distribution': dict(true_dist) if 'category' in df.columns else {},
            'mapped_accuracy': accuracy if len(true_labels) > 0 else None,
            'sample_size': len(our_results)
        }