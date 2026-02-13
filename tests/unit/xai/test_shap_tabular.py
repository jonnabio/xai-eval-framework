"""
Unit tests for the SHAP Tabular Wrapper (EXP1-13).
"""
import pytest
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from src.xai.shap_tabular import (
    SHAPTabularWrapper, 
    generate_shap_explanations, 
    sample_background_data,
    validate_shap_additivity
)
import shap

# --- Fixtures ---

@pytest.fixture(scope="module")
def sample_data():
    """Provides valid training data and feature names."""
    n_samples = 50
    n_features = 4
    X = np.random.rand(n_samples, n_features)
    feature_names = [f"f{i}" for i in range(n_features)]
    # Binary targets for stratify test
    y = np.random.randint(0, 2, n_samples)
    return X, y, feature_names

@pytest.fixture(scope="module")
def trained_tree_model(sample_data):
    """Provides a fitted sklearn DecisionTree for TreeExplainer testing."""
    X, y, _ = sample_data
    model = DecisionTreeClassifier(random_state=42, max_depth=2)
    model.fit(X, y)
    return model

# --- Utility Tests ---

def test_sample_background_data(sample_data):
    """Test background sampling utility."""
    X, y, _ = sample_data
    
    # 1. Random sampling
    bg = sample_background_data(X, n_samples=10, random_state=42)
    assert bg.shape == (10, X.shape[1])
    
    # 2. Stratified sampling
    bg_strat = sample_background_data(X, n_samples=10, y=y, stratify=True, random_state=42)
    assert bg_strat.shape == (10, X.shape[1])

def test_validate_shap_additivity():
    """Test additivity validation utility."""
    # Mock data: prediction = 0.8, base = 0.5 -> sum(shap) should be 0.3
    shap_values = np.array([[0.1, 0.1, 0.1]]) # sum = 0.3
    expected_value = 0.5
    predictions = np.array([0.8])
    
    is_valid, max_error = validate_shap_additivity(shap_values, expected_value, predictions)
    assert is_valid
    assert max_error < 1e-5
    
    # Fail case
    is_valid_fail, _ = validate_shap_additivity(shap_values, expected_value, np.array([0.9]))
    assert not is_valid_fail

# --- Wrapper Tests ---

class TestSHAPTabularWrapper:
    
    def test_initialization(self, sample_data, trained_tree_model):
        """Test wrapper initializes TreeExplainer correctly."""
        X, _, features = sample_data
        
        wrapper = SHAPTabularWrapper(
            model=trained_tree_model,
            training_data=X,
            feature_names=features,
            model_type="tree",
            n_background_samples=10
        )
        
        assert wrapper.model_type == "tree"
        assert wrapper.background_data.shape == (10, len(features))
        assert isinstance(wrapper.expected_value, float)

    def test_generate_explanations_shape(self, sample_data, trained_tree_model):
        """Test explanation generation output shapes."""
        X, _, features = sample_data
        
        wrapper = SHAPTabularWrapper(trained_tree_model, X, features, n_background_samples=10)
        
        # Explain 5 instances
        X_test = X[:5]
        results = wrapper.generate_explanations(trained_tree_model, X_test)
        
        assert "feature_importance" in results
        assert results["feature_importance"].shape == (5, len(features))
        assert results["top_features"].shape == (5, len(features))
        assert "metadata" in results

    def test_explain_instance(self, sample_data, trained_tree_model):
        """Test single instance wrapper."""
        X, _, features = sample_data
        wrapper = SHAPTabularWrapper(trained_tree_model, X, features, n_background_samples=10)
        
        instance = X[0]
        imp_vector = wrapper.explain_instance(trained_tree_model, instance)
        
        assert imp_vector.shape == (len(features),)

    def test_consistency(self, sample_data, trained_tree_model):
        """Test that fixed seeds produce consistent background and explanations (TreeExplainer is exact given bg)."""
        X, _, features = sample_data # background data is sampled from here
        X_test = X[:1]
        
        w1 = SHAPTabularWrapper(trained_tree_model, X, features, random_state=42)
        r1 = w1.generate_explanations(trained_tree_model, X_test)["feature_importance"]
        
        w2 = SHAPTabularWrapper(trained_tree_model, X, features, random_state=42)
        r2 = w2.generate_explanations(trained_tree_model, X_test)["feature_importance"]
        
        np.testing.assert_array_almost_equal(r1, r2)
        
    def test_convenience_function(self, sample_data, trained_tree_model):
        """Test the standalone factory function."""
        X, _, features = sample_data
        
        result = generate_shap_explanations(
            model=trained_tree_model,
            X_samples=X[:2],
            training_data=X,
            feature_names=features,
            n_background_samples=5
        )
        
        assert result["feature_importance"].shape == (2, len(features))

    def test_kmeans_initialization(self, sample_data, trained_tree_model):
        """Test wrapper initializes with K-Means summarization when requested."""
        X, _, features = sample_data
        
        # Test with KernelExplainer (usually where K-Means is used)
        if not hasattr(trained_tree_model, 'predict_proba'):
             pytest.skip("Model needs predict_proba for KernelExplainer test")

        n_centroids = 5
        wrapper = SHAPTabularWrapper(
            model=trained_tree_model,
            training_data=X,
            feature_names=features,
            model_type="kernel",
            n_background_samples=n_centroids,
            use_kmeans=True
        )
        
        assert wrapper.use_kmeans is True
        # shap.kmeans returns a custom object (usually DenseData)
        # We verify it has a .data attribute and correct shape
        assert not isinstance(wrapper.background_data, np.ndarray)
        assert hasattr(wrapper.background_data, 'data')
        assert wrapper.background_data.data.shape[0] == n_centroids
        
        # Verify it runs
        try:
            instance = X[0]
            imp_vector = wrapper.explain_instance(trained_tree_model, instance)
            assert imp_vector.shape == (len(features),)
        except Exception as e:
            pytest.fail(f"Explainer failed with K-Means data: {e}")
