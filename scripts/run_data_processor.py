"""Script to run dataset analyzer"""

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
    print("✅ All imports successful")
    
    # Initialize services
    sentiment_service = SentimentService()
    analyzer = DatasetAnalyzer(sentiment_service)
    
    # Check for CSV files
    data_dir = os.path.join(project_root, "data")
    if os.path.exists(data_dir):
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        if csv_files:
            print("CSV files found:")
            for i, file in enumerate(csv_files, 1):
                print(f"   {i}. {file}")
            
            # Analyze first file
            first_file = os.path.join(data_dir, csv_files[0])
            
            print("\n" + "="*50)
            print("ANALYZING DATASET (without corrupting our system)")
            print("="*50)
            
            # Run comparison
            results = analyzer.analyze_dataset_comparison(first_file, sample_size=100)
            
            # Generate business insights
            print("\n" + "="*50)
            insights = analyzer.generate_insights_report(first_file, sample_size=200)
            
        else:
            print("No CSV files found")
    else:
        print("Data folder not found")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()