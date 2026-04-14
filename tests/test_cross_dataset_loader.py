import numpy as np
import pytest

from src.data_loading.cross_dataset import load_breast_cancer, load_tabular_dataset


def test_load_breast_cancer_shapes(tmp_path):
    preprocessor_path = tmp_path / "preprocessor.joblib"

    X_train, X_test, y_train, y_test, feature_names, _ = load_breast_cancer(
        random_state=42,
        preprocessor_path=str(preprocessor_path),
        verbose=False,
    )

    assert X_train.shape[1] == len(feature_names)
    assert X_test.shape[1] == len(feature_names)
    assert X_train.shape[0] == y_train.shape[0]
    assert X_test.shape[0] == y_test.shape[0]
    assert set(np.unique(y_train)).issubset({0, 1})
    assert set(np.unique(y_test)).issubset({0, 1})
    assert not np.isnan(X_train).any()
    assert not np.isnan(X_test).any()
    assert preprocessor_path.exists()


def test_load_tabular_dataset_dispatches_breast_cancer(tmp_path):
    X_train, X_test, _, _, feature_names, _ = load_tabular_dataset(
        "breast_cancer",
        random_state=123,
        preprocessor_path=str(tmp_path / "preprocessor.joblib"),
        verbose=False,
    )

    assert X_train.shape[1] == X_test.shape[1] == len(feature_names)


def test_load_tabular_dataset_rejects_unknown_dataset():
    with pytest.raises(ValueError, match="Unsupported EXP3 dataset"):
        load_tabular_dataset("not_a_dataset", verbose=False)
