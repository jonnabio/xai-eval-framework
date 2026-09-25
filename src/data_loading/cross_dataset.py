"""
Cross-dataset tabular loaders for EXP3 external validation.

This module provides compact, binary-classification loaders that mirror the
tuple contract used by ``load_adult``:

``(X_train, X_test, y_train, y_test, feature_names, preprocessor)``.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple
from urllib.request import urlopen

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from scipy.io import arff
from sklearn.datasets import load_breast_cancer as sklearn_load_breast_cancer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

logger = logging.getLogger(__name__)

TabularSplit = Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, List[str], ColumnTransformer]
GERMAN_CREDIT_ARFF_URL = "https://www.openml.org/data/download/31/dataset_31_credit-g.arff"


def _coerce_binary_target(y: pd.Series, positive_label: Optional[str] = None) -> pd.Series:
    """
    Convert a binary target series to integer labels.

    Args:
        y: Raw target labels.
        positive_label: Optional label to map to 1.

    Returns:
        Integer target series containing only 0 and 1.
    """
    if pd.api.types.is_numeric_dtype(y):
        unique_values = sorted(pd.Series(y).dropna().unique().tolist())
        if len(unique_values) != 2:
            raise ValueError(f"Expected binary target, found values: {unique_values}")
        return pd.Series(y).map({unique_values[0]: 0, unique_values[1]: 1}).astype(int)

    y_str = pd.Series(y).astype(str).str.strip()
    unique_values = sorted(y_str.dropna().unique().tolist())
    if len(unique_values) != 2:
        raise ValueError(f"Expected binary target, found values: {unique_values}")

    if positive_label is None:
        positive_label = unique_values[-1]

    if positive_label not in unique_values:
        raise ValueError(f"Positive label {positive_label!r} not in target values: {unique_values}")

    return (y_str == positive_label).astype(int)


def _decode_arff_frame(path: Path) -> pd.DataFrame:
    """Load an ARFF file into a pandas frame with byte labels decoded."""
    data, _ = arff.loadarff(path)
    frame = pd.DataFrame(data)
    for column in frame.columns:
        if frame[column].dtype == object:
            frame[column] = frame[column].map(
                lambda value: value.decode("utf-8") if isinstance(value, bytes) else value
            )
    return frame


def _load_cached_german_credit_arff(cache_dir: str) -> pd.DataFrame:
    """Load German Credit from a cached direct OpenML ARFF download."""
    arff_path = Path(cache_dir) / "openml" / "dataset_31_credit-g.arff"
    if not arff_path.exists():
        arff_path.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(GERMAN_CREDIT_ARFF_URL, timeout=30) as response:
            arff_path.write_bytes(response.read())
    return _decode_arff_frame(arff_path)


def _split_feature_types(X: pd.DataFrame) -> tuple[List[str], List[str]]:
    """Return numeric and categorical column names for a tabular DataFrame."""
    numeric_features = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = [col for col in X.columns if col not in numeric_features]
    return numeric_features, categorical_features


def _create_preprocessor(
    numeric_features: List[str], categorical_features: List[str]
) -> ColumnTransformer:
    """Create a fitted-later preprocessing pipeline for mixed tabular data."""
    transformers = []

    if numeric_features:
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        transformers.append(("num", numeric_transformer, numeric_features))

    if categorical_features:
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]
        )
        transformers.append(("cat", categorical_transformer, categorical_features))

    if not transformers:
        raise ValueError("No features available for preprocessing")

    return ColumnTransformer(transformers=transformers, verbose_feature_names_out=False)


def _get_feature_names(
    preprocessor: ColumnTransformer,
    numeric_features: List[str],
    categorical_features: List[str],
) -> List[str]:
    """Extract transformed feature names from a fitted preprocessor."""
    feature_names: List[str] = []
    if numeric_features:
        feature_names.extend(numeric_features)

    if categorical_features:
        try:
            cat_pipeline = preprocessor.named_transformers_["cat"]
            ohe = cat_pipeline.named_steps["onehot"]
            feature_names.extend(ohe.get_feature_names_out(categorical_features).tolist())
        except Exception as exc:
            logger.warning("Failed to extract categorical feature names: %s", exc)
            feature_names.extend(categorical_features)

    return feature_names


def _prepare_tabular_split(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    test_size: float,
    random_state: int,
    preprocessor: Optional[ColumnTransformer] = None,
    preprocessor_path: Optional[str] = None,
) -> TabularSplit:
    """Split, preprocess, and optionally persist a tabular binary dataset."""
    X = X.copy()
    y = pd.Series(y).astype(int)

    numeric_features, categorical_features = _split_feature_types(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    created_preprocessor = preprocessor is None
    if preprocessor is None:
        preprocessor = _create_preprocessor(numeric_features, categorical_features)
        X_train_processed = preprocessor.fit_transform(X_train)
    else:
        X_train_processed = preprocessor.transform(X_train)

    X_test_processed = preprocessor.transform(X_test)
    feature_names = _get_feature_names(preprocessor, numeric_features, categorical_features)

    if preprocessor_path and created_preprocessor:
        path = Path(preprocessor_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(preprocessor, path)
        logger.info("Saved preprocessor to %s", path)

    return (
        np.asarray(X_train_processed, dtype=float),
        np.asarray(X_test_processed, dtype=float),
        y_train.to_numpy(dtype=int),
        y_test.to_numpy(dtype=int),
        feature_names,
        preprocessor,
    )


def load_breast_cancer(
    test_size: float = 0.2,
    random_state: int = 42,
    cache_dir: str = "./data",
    preprocessor_path: Optional[str] = None,
    verbose: bool = True,
    preprocessor: Optional[ColumnTransformer] = None,
) -> TabularSplit:
    """
    Load the sklearn Breast Cancer Wisconsin dataset for EXP3.

    Args:
        test_size: Proportion of rows reserved for test evaluation.
        random_state: Split seed.
        cache_dir: Unused compatibility argument.
        preprocessor_path: Optional path to save a newly fitted preprocessor.
        verbose: Whether to emit informational logs.
        preprocessor: Optional pre-fitted preprocessor to reuse.

    Returns:
        Processed train/test split and fitted preprocessor.
    """
    if verbose:
        logger.info("Loading Breast Cancer dataset for EXP3")
    dataset = sklearn_load_breast_cancer(as_frame=True)
    X = dataset.data
    y = pd.Series(dataset.target, name="target")
    return _prepare_tabular_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        preprocessor=preprocessor,
        preprocessor_path=preprocessor_path,
    )


def load_german_credit(
    test_size: float = 0.2,
    random_state: int = 42,
    cache_dir: str = "./data",
    preprocessor_path: Optional[str] = None,
    verbose: bool = True,
    preprocessor: Optional[ColumnTransformer] = None,
) -> TabularSplit:
    """
    Load the OpenML German Credit dataset for EXP3.

    The OpenML target labels are mapped so ``good`` is the positive class.
    """
    if verbose:
        logger.info("Loading German Credit dataset from OpenML for EXP3")
    frame = _load_cached_german_credit_arff(cache_dir)
    X = frame.drop(columns=["class"])
    y = _coerce_binary_target(pd.Series(frame["class"], name="target"), positive_label="good")
    return _prepare_tabular_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        preprocessor=preprocessor,
        preprocessor_path=preprocessor_path,
    )


LOADERS: Dict[str, Callable[..., TabularSplit]] = {
    "breast_cancer": load_breast_cancer,
    "german_credit": load_german_credit,
}


def load_tabular_dataset(dataset: str, **kwargs) -> TabularSplit:
    """
    Dispatch to a supported EXP3 tabular dataset loader.

    Args:
        dataset: Dataset key such as ``breast_cancer`` or ``german_credit``.
        **kwargs: Loader options passed through to the selected loader.

    Returns:
        Processed train/test split and fitted preprocessor.
    """
    key = dataset.lower()
    try:
        loader = LOADERS[key]
    except KeyError as exc:
        raise ValueError(f"Unsupported EXP3 dataset: {dataset}") from exc
    return loader(**kwargs)
