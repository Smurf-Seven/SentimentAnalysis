"""Test script for Reddit sentiment dataset"""

import sys
import os

# Get paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
src_path = os.path.join(project_root, 'src')

sys.path.insert(0, src_path)
sys.path.insert(0, project_root)

try:
    from services.sentiment_service import SentimentService
    from services.dataset_analyzer import DatasetAnalyzer
    print("✅ BERT system imported successfully")
    
    # Initialize services
    sentiment_service = SentimentService()
    analyzer = DatasetAnalyzer(sentiment_service)
    
    # Test Reddit dataset
    reddit_file = os.path.join(project_root, "data", "Twitter_Data.csv")
    
    if os.path.exists(reddit_file):
        print("\n" + "="*50)
        print("TESTING REDDIT DATASET (-1,0,1 LABELS)")
        print("="*50)
        
        # Analyze Reddit dataset
        results = analyzer.analyze_reddit_dataset(reddit_file, sample_size=100)
        
        if results:
            print(f"\n🎯 REDDIT ANALYSIS COMPLETED!")
            if results.get('mapped_accuracy'):
                print(f"📊 Mapped Accuracy: {results['mapped_accuracy']:.2%}")
    else:
        print(f"❌ Reddit dataset not found: {reddit_file}")
        print("💡 Download 'Reddit_Data.csv' and place it in the 'data' folder")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()