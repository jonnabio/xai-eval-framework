"""
Module for loading and preprocessing the UCI Adult dataset.

This module provides functionality to load the Adult Income dataset,
define its schema (column names, feature types), and preprocess it
for machine learning tasks.
"""

import logging
import hashlib
import json
import urllib.request
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import shutil

import numpy as np
import pandas as pd
import joblib
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from src.data_loading.data_config import ADULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Dataset Constants (kept for backward compatibility/direct access)
COLUMN_NAMES: List[str] = ADULT_CONFIG["column_names"]

NUMERIC_FEATURES: List[str] = [
    "age", "fnlwgt", "education-num", "capital-gain", "capital-loss", "hours-per-week"
]

CATEGORICAL_FEATURES: List[str] = [
    "workclass", "education", "marital-status", "occupation",
    "relationship", "race", "sex", "native-country"
]

TARGET_COLUMN: str = "income"


def _compute_checksum(filepath: Path) -> str:
    """Calculate SHA256 hash of file for integrity checking."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def _validate_cache(cache_dir: Path) -> Optional[pd.DataFrame]:
    """
    Check for cached data files and validate them.
    
    Args:
        cache_dir: Directory to check for cached files.
        
    Returns:
        pd.DataFrame if valid cache found, None otherwise.
    """
    logger.info(f"Checking cache at: {cache_dir}")
    
    # Check for parquet (preferred) or csv
    parquet_path = cache_dir / "adult.parquet"
    metadata_path = cache_dir / "adult_metadata.json"
    
    if not parquet_path.exists():
        logger.info("Cache validation: MISSING (no data file)")
        return None
        
    if not metadata_path.exists():
        logger.warning("Cache validation: MISSING METADATA (found data but no metadata)")
        # If we have data but no metadata, we might still try to load it if desperate,
        # but for robustness let's return None to trigger re-download/validation
        return None
        
    try:
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        # Verify checksum
        current_checksum = _compute_checksum(parquet_path)
        if current_checksum != metadata.get("checksum"):
            logger.warning(f"Cache validation: CHECKSUM MISMATCH (stored: {metadata.get('checksum')}, calculated: {current_checksum})")
            return None
            
        logger.info(f"Cache validation: VALID (checksum: match)")
        
        # Load data
        df = pd.read_parquet(parquet_path)
        return df
        
    except Exception as e:
        logger.error(f"Cache validation failed with error: {e}")
        return None


def _save_with_metadata(df: pd.DataFrame, cache_dir: Path, source: str) -> None:
    """
    Save DataFrame to cache with metadata.
    
    Args:
        df: DataFrame to save.
        cache_dir: Directory to save to.
        source: Source identifier string.
    """
    # Check disk space (simple check using shutil)
    total, used, free = shutil.disk_usage(cache_dir)
    # Estimate size (very rough: rows * cols * 8 bytes + overhead)
    estimated_size = df.memory_usage(deep=True).sum()
    if free < estimated_size * 2:
        logger.warning("Low disk space, might fail to save cache.")

    parquet_path = cache_dir / "adult.parquet"
    csv_path = cache_dir / "adult.csv"
    metadata_path = cache_dir / "adult_metadata.json"
    
    try:
        # Save as Parquet (efficient)
        df.to_parquet(parquet_path, index=False)
        file_size_mb = parquet_path.stat().st_size / (1024 * 1024)
        logger.info(f"Saved to cache: {parquet_path.name} ({file_size_mb:.1f} MB)")
        
        # Save as CSV (human readable backup/flexibility)
        df.to_csv(csv_path, index=False)
        
        # Compute checksum of the primary parquet file
        checksum = _compute_checksum(parquet_path)
        
        # Save metadata
        metadata = {
            "download_date": datetime.now().isoformat(),
            "source": source,
            "shape": df.shape,
            "columns": list(df.columns),
            "checksum": checksum,
            "versions": {
                "pandas": pd.__version__,
                "numpy": np.__version__
            }
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
            
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")


def _validate_dataframe(df: pd.DataFrame) -> bool:
    """
    Validate downloaded dataframe against expectations.
    
    Args:
        df: DataFrame to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    # Check shape
    rows, cols = df.shape
    if rows < ADULT_CONFIG["min_rows"]:
        logger.error(f"Validation failed: Too few rows ({rows} < {ADULT_CONFIG['min_rows']})")
        return False
        
    if cols != ADULT_CONFIG["expected_cols"]:
        logger.error(f"Validation failed: Unexpected column count ({cols} != {ADULT_CONFIG['expected_cols']})")
        return False
    
    # Verify no completely empty columns
    if df.isnull().all().any():
        logger.error("Validation failed: Found completely empty columns")
        return False
        
    # Check expected column names can be assigned/are present
    # Note: If loading from OpenML, cols might be different initially, 
    # but we assume this runs after column renaming if needed.
    # For now, just check specific critical columns if they exist
    # or if we are about to overwrite them.
    
    logger.info(f"Validation passed: {rows} rows, {cols} columns")
    return True


def _download_from_openml(cache_dir: Path) -> Optional[pd.DataFrame]:
    """Download dataset from OpenML."""
    logger.info("Downloading from openml_v2...")
    try:
        # fetch_openml handles caching internally if data_home is set, 
        # but we manage our own structure so we might just use it to fetch.
        # We explicitly set data_home to a temp or internal dir if we wanted sklearn to cache,
        # but here we pass cache_dir so sklearn puts it there. 
        # Sklearn structure is different, so we'll just extract the DF.
        
        # Note: OpenML 'adult' v2 usually has 'income' as target but sometimes separate.
        # as_frame=True returns a bunch object with 'frame' or 'data'/'target'
        
        start_time = time.time()
        # Set 30s timeout for the request (implicit in sklearn/urlopen via socket usually, 
        # but difficult to enforce strictly without socket.setdefaulttimeout)
        
        dataset = fetch_openml(
            data_id=1590, # ID for adult v2
            data_home=str(cache_dir / "sklearn_cache"),
            as_frame=True,
            parser='auto',
            return_X_y=False
        )
        
        if dataset.frame is not None:
            df = dataset.frame
        else:
            # Combine X and y
            X = dataset.data
            y = dataset.target
            df = pd.concat([X, y], axis=1)
            
        elapsed = time.time() - start_time
        logger.info(f"OpenML download completed in {elapsed:.1f}s")
        
        # Ensure column names match our config standard
        # OpenML columns are usually consistent but let's be safe
        if len(df.columns) == len(ADULT_CONFIG["column_names"]):
            df.columns = ADULT_CONFIG["column_names"]
            
        return df
        
    except Exception as e:
        logger.warning(f"OpenML download failed: {e}")
        return None


def _download_from_uci(cache_dir: Path) -> Optional[pd.DataFrame]:
    """Download dataset directly from UCI repository."""
    logger.info("Downloading from uci_direct...")
    
    urls = {
        "train": ADULT_CONFIG["sources"]["uci_data"],
        "test": ADULT_CONFIG["sources"]["uci_test"]
    }
    
    dataframes = []
    
    for split, url in urls.items():
        try:
            logger.info(f"Fetching {split} set from {url}...")
            
            # 3 retries
            for attempt in range(3):
                try:
                    df_part = pd.read_csv(
                        url, 
                        header=None, 
                        names=ADULT_CONFIG["column_names"],
                        na_values=["?", " ?"],
                        skipinitialspace=True,
                        engine='python' # More robust separator handling
                    )
                    
                    # UCI test file has a weird first line sometimes or dot at end of class
                    if split == "test":
                        # First line often "1x3 Cross validator" noise or just data
                        # We'll filter based on expected bad lines if needed, but usually read_csv is okay
                        # Adult test set target has a dot '.' at the end, e.g. '<=50K.'
                        if df_part[TARGET_COLUMN].dtype == 'object':
                            df_part[TARGET_COLUMN] = df_part[TARGET_COLUMN].str.rstrip('.')
                            
                    dataframes.append(df_part)
                    break # Success
                except Exception as e:
                    if attempt == 2:
                        raise e
                    time.sleep(1)
                    
        except Exception as e:
            logger.warning(f"Failed to download {split} from UCI: {e}")
            return None
            
    if len(dataframes) != 2:
        return None
        
    # Combine train and test
    full_df = pd.concat(dataframes, ignore_index=True)
    return full_df


def _fetch_adult_data(cache_dir: str = None) -> pd.DataFrame:
    """
    Fetch the Adult dataset with robust caching and extensive validation.
    
    Args:
        cache_dir: Optional custom cache directory. Should match config normally.
        
    Returns:
        pd.DataFrame: The raw Adult dataset.
        
    Raises:
        ValueError: If data cannot be obtained from any source.
    """
    # 1. Setup
    if cache_dir is None:
        cache_dir = str(ADULT_CONFIG["cache_dir"])
    cache_path = Path(cache_dir)
    cache_path.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Fetching Adult dataset, cache dir: {cache_path}")
    
    # 2. Try cache first
    cached_df = _validate_cache(cache_path)
    if cached_df is not None:
        logger.info(f"✓ Loaded from cache: {cached_df.shape}")
        return cached_df
    
    # 3. Try downloading from sources
    logger.info("Cache not found/invalid, downloading...")
    
    df = None
    source = "unknown"
    
    # Try OpenML first (cleanest source)
    df = _download_from_openml(cache_path)
    source = "openml_v2"
    
    # Fallback to UCI
    if df is None:
        logger.warning("OpenML failed, trying UCI repository...")
        df = _download_from_uci(cache_path)
        source = "uci_direct"
    
    # 4. Validate
    if df is None:
        raise ValueError("Failed to download Adult dataset from all sources")
    
    if not _validate_dataframe(df):
        raise ValueError(f"Downloaded data validation failed: shape={df.shape}")
    
    # 5. Save with metadata
    _save_with_metadata(df, cache_path, source)
    logger.info(f"✓ Downloaded and cached: {df.shape}")
    
    return df


def ensure_adult_data_dirs() -> None:
    """Create required directories and documentation."""
    dirs = [
        ADULT_CONFIG["cache_dir"],
        # Ensure the exp1 specific dirs exist too as this is the loader for it
        Path("experiments/exp1_adult/models"),
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    # Create README in data dir
    readme = ADULT_CONFIG["cache_dir"] / "README.md"
    if not readme.exists():
        readme.write_text("# Adult Dataset\n\nCached UCI Adult dataset files.\nDo not commit to git!")


def _clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the Adult dataset.
    
    Operations:
    1. Strip whitespace from string columns.
    2. Replace ' ?' with np.nan.
    3. Encode target 'income' to 0 (<=50K) and 1 (>50K).
    4. Remove duplicates.
    5. Cast numeric columns to numeric types.
    
    Args:
        df: Raw DataFrame.
        
    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    initial_rows = len(df)
    logger.info(f"Cleaning data (initial shape: {df.shape})...")
    
    # 1. Strip whitespace from object columns
    # Many UCI datasets have space padding like ' Private' instead of 'Private'
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype(str).str.strip()
        
    # 2. Handle missing values ('?')
    # Replace '?' or '?' with np.nan
    df = df.replace(['?', ' ?'], np.nan)
    
    # 3. Encode target variable
    # Standardize to 0/1. Handle potential dots or variations if any remained.
    # Expected values: '<=50K', '>50K', '<=50K.', '>50K.'
    
    # First ensure it's string and stripped (already done above)
    # Map valid values
    income_map = {
        '<=50K': 0,
        '<=50K.': 0,
        '>50K': 1,
        '>50K.': 1
    }
    
    # Check if target contains values outside our map
    unique_targets = df[TARGET_COLUMN].unique()
    logger.info(f"Unique target values found: {unique_targets}")
    
    # Apply mapping
    # Coerce errors to NaN if something unexpected, but we should probably handle it
    df[TARGET_COLUMN] = df[TARGET_COLUMN].map(income_map)
    
    # Drop rows where target became NaN (shouldn't happen if map covers all)
    if df[TARGET_COLUMN].isna().any():
        n_missing_target = df[TARGET_COLUMN].isna().sum()
        logger.warning(f"dropped {n_missing_target} rows with invalid target values")
        df = df.dropna(subset=[TARGET_COLUMN])
        
    df[TARGET_COLUMN] = df[TARGET_COLUMN].astype(int)
    
    # 4. Remove exact duplicate rows
    df = df.drop_duplicates()
    
    # 5. Ensure numeric columns are numeric
    # sometimes '?' makes them object
    for col in NUMERIC_FEATURES:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    # Log results
    final_rows = len(df)
    removed_rows = initial_rows - final_rows
    logger.info(f"Cleaned data: Removed {removed_rows} rows (duplicates or bad target). Final shape: {df.shape}")
    
    return df


def _create_preprocessor() -> ColumnTransformer:
    """
    Create a sklearn preprocessing pipeline for the Adult dataset.
    
    Returns:
        ColumnTransformer: Unfitted preprocessor.
    """
    # 1. Numeric pipeline
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])
    
    # 2. Categorical pipeline
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])
    
    # 3. Combine
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, NUMERIC_FEATURES),
            ('cat', categorical_transformer, CATEGORICAL_FEATURES)
        ],
        verbose_feature_names_out=False
    )
    
    return preprocessor


def _get_feature_names(preprocessor: ColumnTransformer, input_features: List[str]) -> List[str]:
    """
    Extract feature names from the preprocessor.
    
    Args:
        preprocessor: Fitted ColumnTransformer.
        input_features: List of input feature names.
        
    Returns:
        List of output feature names.
    """
    output_features = []
    
    # 1. Numeric features (usually unchanged by StandardScaler, just scaled)
    # The 'num' transformer corresponds to NUMERIC_FEATURES
    output_features.extend(NUMERIC_FEATURES)
    
    # 2. Categorical features (OneHotEncoded)
    # The 'cat' transformer is the second one (index 1) in our pipeline
    # We need to access the OneHotEncoder step
    try:
        # Access the 'cat' pipeline
        cat_pipeline = preprocessor.named_transformers_['cat']
        # Access the 'onehot' step within that pipeline
        ohe = cat_pipeline.named_steps['onehot']
        
        # Get feature names
        # We need to provide the input feature names for the categorical columns
        cat_feature_names = ohe.get_feature_names_out(CATEGORICAL_FEATURES)
        output_features.extend(cat_feature_names)
        
    except Exception as e:
        logger.warning(f"Failed to extract categorical feature names: {e}")
        # Fallback: keep original names (incorrect for OHE but better than nothing)
        output_features.extend(CATEGORICAL_FEATURES)
        
    return output_features


def load_adult(test_size: float = 0.2, random_state: int = 42, cache_dir: str = "./data", 
               preprocessor_path: str = None, verbose: bool = True) -> tuple:
    """
    Load, clean, and split the Adult dataset.
    
    Args:
        test_size: Proportion of dataset to include in the test split.
        random_state: Random seed for reproducibility.
        cache_dir: Directory to cache downloaded data.
        preprocessor_path: Path to save/load the preprocessor (not implemented yet).
        verbose: Whether to print logs.
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test) as pandas objects.
    """
    if verbose:
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.getLogger().setLevel(logging.WARNING)
        
    logger.info("Starting Adult dataset loading pipeline...")
    
    # 1. Fetch raw data
    raw_df = _fetch_adult_data(cache_dir=cache_dir)
    
    # 2. Clean data
    clean_df = _clean_data(raw_df)
    
    # 3. Separate Features and Target
    X = clean_df.drop(columns=[TARGET_COLUMN])
    y = clean_df[TARGET_COLUMN]
    
    logger.info(f"Data separation complete: X.shape={X.shape}, y.shape={y.shape}")
    logger.info(f"Target distribution:\n{y.value_counts(normalize=True)}")
    
    # 4. Split data (Stratified)
    logger.info(f"Splitting data (test_size={test_size}, stratify=True)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # 5. Preprocessing
    logger.info("Preprocessing data...")
    preprocessor = _create_preprocessor()
    
    # Fit on training data
    logger.info("Fitting preprocessor on training data...")
    X_train_processed = preprocessor.fit_transform(X_train)
    
    # Transform test data
    logger.info("Transforming test data...")
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names
    feature_names = _get_feature_names(preprocessor, X.columns.tolist())
    
    # 6. Save preprocessor if requested
    if preprocessor_path:
        path = Path(preprocessor_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(preprocessor, path)
        logger.info(f"Saved preprocessor to {path}")
        
    # 7. Validation
    # Check for NaNs in processed data
    # (StandardScaler handles NaNs if with_mean=False, but we used True (default). 
    #  OHE handles handle_unknown='ignore'.
    #  We already cleaned NaNs in _clean_data, so we should be safe.)
    
    # Convert sparse matrices to dense if needed (though we set sparse_output=False in OHE)
    # StandardScaler output is dense.
    
    if np.isnan(X_train_processed).any():
        logger.warning("NaNs found in processed training data!")
    
    if np.isnan(X_test_processed).any():
        logger.warning("NaNs found in processed test data!")

    if verbose:
        logger.info(f"Processed Train shape: {X_train_processed.shape}")
        logger.info(f"Processed Test shape:  {X_test_processed.shape}")
        logger.info(f"Feature count: {len(feature_names)}")
        
    return X_train_processed, X_test_processed, y_train, y_test, feature_names, preprocessor


def load_preprocessor(path: str) -> Pipeline:
    """
    Load a saved preprocessor pipeline.
    
    Args:
        path: Path to the saved joblib file.
        
    Returns:
        Pipeline: Loaded sklearn pipeline.
        
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Preprocessor not found at {path}")
        
    try:
        return joblib.load(p)
    except Exception as e:
        logger.error(f"Failed to load preprocessor: {e}")
        raise e


def get_original_feature_names() -> tuple[List[str], List[str]]:
    """
    Get the original numeric and categorical feature names.
    
    Returns:
        tuple[List[str], List[str]]: (numeric_features, categorical_features)
    """
    return list(NUMERIC_FEATURES), list(CATEGORICAL_FEATURES)


# Call on module import to ensure structure
ensure_adult_data_dirs()
