import unittest
import numpy as np
from src.metrics.faithfulness import FaithfulnessMetric

class MockModel:
    def predict_proba(self, X):
        # Dummy prediction: average of first 3 features
        # If feature 0 is removed (masked), prediction should change
        return np.array([[0, np.mean(x[:3])] for x in X])

    def predict(self, X):
        return self.predict_proba(X)[:, 1]

class TestFaithfulnessMetric(unittest.TestCase):
    def setUp(self):
        self.metric = FaithfulnessMetric(top_k=2)
        # Baseline = zeros
        self.X_train = np.zeros((10, 5))
        self.metric.set_baseline(self.X_train)

    def test_faithfulness_gap(self):
        # Instance: [1, 1, 1, 0, 0]
        # Prediction: mean(1,1,1) = 1.0
        instance = np.array([1, 1, 1, 0, 0])
        model = MockModel()
        
        # Explanation: Feat 0 and 1 are important
        explanation = np.array([0.5, 0.5, 0.1, 0, 0])
        
        # Masked: [0, 0, 1, 0, 0] (Top 2 masked)
        # Prediction: mean(0,0,1) = 0.33
        
        # Gap should be |1.0 - 0.33| = 0.66
        
        res = self.metric.compute(explanation, model=model, data=instance)
        
        print(f"Computed res: {res}")
        self.assertTrue('faithfulness_gap' in res)
        self.assertAlmostEqual(res['faithfulness_gap'], 0.666, places=2)
        
    def test_faithfulness_corr(self):
        # Instance: [1, 1, 1, 1, 1]
        instance = np.ones(5)
        model = MockModel() # pred = mean(x[:3])
        
        # Exp weights: [0.5, 0.4, 0.1, 0.0, 0.0]
        explanation = np.array([0.5, 0.4, 0.1, 0.0, 0.0])
        
        # Drops:
        # F0 masked -> [0,1,1..] -> pred 0.66 (drop 0.33)
        # F1 masked -> [1,0,1..] -> pred 0.66 (drop 0.33)
        # F2 masked -> [1,1,0..] -> pred 0.66 (drop 0.33)
        # F3 masked -> [1,1,1,0..] -> pred 1.0 (drop 0)
        # F4 masked -> [1,1,1,1,0] -> pred 1.0 (drop 0)
        
        # Drops: [0.33, 0.33, 0.33, 0, 0]
        # Weights: [0.5, 0.4, 0.1, 0, 0]
        # Correlation should be high positive
        
        res = self.metric.compute(explanation, model=model, data=instance)
        self.assertGreater(res['faithfulness_corr'], 0.5)

if __name__ == '__main__':
    unittest.main()
