import sys
import os
import logging
import numpy as np
import pandas as pd
from pathlib import Path

# Add project root to path to ensure imports work when run standalone
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

try:
    from src.data_loading.adult import load_adult
except ImportError:
    print("Error: Could not import 'src.data_loading.adult'. check your python path.")
    sys.exit(1)

# Configure logging to print to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Usage Example: Adult Data Loader")
    
    # Define paths
    # Using a temp directory for the preprocessor to avoid cluttering real results
    preprocessor_path = project_root / "experiments/exp1_adult/models/preprocessor_example.joblib"
    
    try:
        # Call load_adult with all parameters
        logger.info("Calling load_adult()...")
        X_train, X_test, y_train, y_test, feature_names, preprocessor = load_adult(
            test_size=0.2,
            random_state=42,
            # We rely on default cache_dir from config or override if needed
            # cache_dir = "./data", 
            preprocessor_path=str(preprocessor_path),
            verbose=True
        )
        
        print("\n" + "="*50)
        print("DATASET STATISTICS")
        print("="*50)
        
        # 1. Dataset Sizes
        print(f"\n[Sizes]")
        print(f"Train samples: {X_train.shape[0]}")
        print(f"Test samples:  {X_test.shape[0]}")
        print(f"Total samples: {X_train.shape[0] + X_test.shape[0]}")
        
        # 2. Features
        print(f"\n[Features]")
        print(f"Total features: {len(feature_names)}")
        print(f"Feature matrix shape (Train): {X_train.shape}")
        
        print(f"Sample feature names (first 10):")
        for i, name in enumerate(feature_names[:10]):
            print(f"  {i}: {name}")
            
        # 3. Class Distribution
        print(f"\n[Class Distribution]")
        train_dist = pd.Series(y_train).value_counts(normalize=True)
        test_dist = pd.Series(y_test).value_counts(normalize=True)
        
        print("Train:")
        print(train_dist)
        print("Test:")
        print(test_dist)
        
        # 4. Preprocessing Confirmation
        print(f"\n[Preprocessing]")
        print(f"Preprocessor object: {type(preprocessor).__name__}")
        print(f"Saved to: {preprocessor_path}")
        print(f"File exists: {preprocessor_path.exists()}")
        
        # Check values are scaled/normalized (roughly)
        # StandardScaler should mean ~0, std ~1 for numeric columns
        # But X contains OHE too.
        # Let's just check bounds or if it looks numeric
        print(f"Data type: {X_train.dtype}")
        print(f"Min value: {X_train.min():.3f}")
        print(f"Max value: {X_train.max():.3f}")
        
        if np.isnan(X_train).any():
            print("WARNING: NaNs found in X_train!")
        else:
            print("Clean: No NaNs found.")
            
        print("="*50 + "\n")
        logger.info("Usage example completed successfully.")
        
    except Exception as e:
        logger.error(f"An error occurred during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    finally:
        # Optional cleanup of the example preprocessor
        if preprocessor_path.exists():
            logger.info(f"Cleaning up: removing {preprocessor_path}")
            # preprocessor_path.unlink() # Uncomment if we strictly want to clean up

if __name__ == "__main__":
    main()
