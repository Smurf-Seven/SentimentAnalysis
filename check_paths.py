"""Check paths and imports"""

import sys
import os

print("=== PATH CHECK ===")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

# Check project structure
project_root = os.getcwd()
src_path = os.path.join(project_root, 'src')

print(f"Project root: {project_root}")
print(f"SRC path: {src_path}")
print(f"SRC exists: {os.path.exists(src_path)}")

if os.path.exists(src_path):
    print("Contents of SRC:")
    for item in os.listdir(src_path):
        print(f"  - {item}")

print("\n=== CHECKING IMPORTS ===")

# Add paths
sys.path.insert(0, src_path)
sys.path.insert(0, project_root)

print("Current sys.path:")
for path in sys.path[:3]:  # Show first 3
    print(f"  - {path}")

# Test imports
try:
    from services.sentiment_service import SentimentService
    print("✅ SentimentService import successful")
except ImportError as e:
    print(f"❌ SentimentService import failed: {e}")

try:
    from models.bert_model import BERTModel
    print("✅ BERTModel import successful")
except ImportError as e:
    print(f"❌ BERTModel import failed: {e}")

print("\n=== CHECKING DATA FOLDER ===")
data_dir = os.path.join(project_root, 'data')
print(f"Data folder: {data_dir}")
print(f"Data exists: {os.path.exists(data_dir)}")

if os.path.exists(data_dir):
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    print(f"CSV files: {csv_files}")