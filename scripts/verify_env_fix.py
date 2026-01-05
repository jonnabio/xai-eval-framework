import sklearn
import lime
import os
import sys
from pathlib import Path

# Add src to path to import config
sys.path.append(str(Path(__file__).parent.parent))

try:
    from src.data_loading.data_config import DATA_ROOT
except ImportError:
    print("Warning: Could not import data_config to verify path")
    DATA_ROOT = "UNKNOWN"

def verify_environment():
    print("=== Environment Verification ===")
    print(f"scikit-learn version: {sklearn.__version__}")
    print(f"lime version: {lime.__version__}")
    print(f"DATA_ROOT resolved to: {DATA_ROOT}")
    
    expected_sklearn = "1.7.1"
    if sklearn.__version__ != expected_sklearn:
        print(f"❌ FAIL: scikit-learn version mismatch. Expected {expected_sklearn}, got {sklearn.__version__}")
    else:
        print("✅ PASS: scikit-learn version matches")
        
    print(f"Current Working Directory: {os.getcwd()}")
    
if __name__ == "__main__":
    verify_environment()
