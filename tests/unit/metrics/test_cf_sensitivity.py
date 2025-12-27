
import unittest
import numpy as np
import pandas as pd
from src.metrics.sensitivity import CounterfactualSensivtyMetric

class TestCounterfactualSensivtyMetric(unittest.TestCase):
    def setUp(self):
        self.metric = CounterfactualSensivtyMetric()
        # Mock feature names
        self.feature_names = ['age', 'income', 'education', 'hours_per_week']
        
    def test_perfect_alignment(self):
        # Explainer says 'age' and 'income' are important
        weights = np.array([0.9, 0.8, 0.1, 0.1]) # age, income top 2
        
        # Original instance
        orig = pd.DataFrame([[25, 50000, 10, 40]], columns=self.feature_names)
        
        # Counterfactual: Age changed 25->30, Income 50k->60k
        cf = pd.DataFrame([[30, 60000, 10, 40]], columns=self.feature_names)
        
        res = self.metric.compute(weights, self.feature_names, orig, cf, k=2)
        
        # Top-K (2) are age, income.
        # Modified in CF are age, income.
        # Overlap = 2.
        # Recall = 2/2 = 1.0
        # Precision = 2/2 = 1.0
        
        self.assertAlmostEqual(res['cf_sensitivity_recall'], 1.0)
        self.assertAlmostEqual(res['cf_sensitivity_precision'], 1.0)

    def test_partial_alignment(self):
        # Explainer: age, education (Top 2)
        weights = np.array([0.9, 0.1, 0.8, 0.0]) # age, education
        
        # Original
        orig = pd.DataFrame([[25, 50000, 10, 40]], columns=self.feature_names)
        
        # CF: Age changed, Hours changed. Education same.
        cf = pd.DataFrame([[30, 50000, 10, 50]], columns=self.feature_names)
        
        res = self.metric.compute(weights, self.feature_names, orig, cf, k=2)
        
        # Top-K: age, education
        # Modified: age, hours_per_week
        # Overlap: age (1)
        
        # Recall (w.r.t Modified): 1 / 2 = 0.5
        # Precision (w.r.t Top-K): 1 / 2 = 0.5
        
        self.assertAlmostEqual(res['cf_sensitivity_recall'], 0.5)

    def test_no_cfs(self):
        weights = np.array([1, 1, 1, 1])
        orig = pd.DataFrame([[1, 1, 1, 1]], columns=self.feature_names)
        cf = pd.DataFrame() # Empty
        
        res = self.metric.compute(weights, self.feature_names, orig, cf)
        self.assertEqual(res['cf_sensitivity'], 0.0)

if __name__ == '__main__':
    unittest.main()
