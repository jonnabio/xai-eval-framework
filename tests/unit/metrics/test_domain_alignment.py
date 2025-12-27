
import unittest
import numpy as np
from src.metrics.domain import DomainAlignmentMetric

class TestDomainAlignmentMetric(unittest.TestCase):
    def setUp(self):
        self.metric = DomainAlignmentMetric()

    def test_precision_recall_perfect(self):
        # 3 Core features: age, education, hours-per-week
        feature_names = ['age', 'education', 'hours-per-week', 'random1', 'random2']
        # Top 3 are all core
        weights = np.array([0.5, 0.4, 0.3, 0.0, 0.0])
        
        res = self.metric.compute(weights, feature_names, k=3)
        
        # Precision: 3/3 = 1.0 (All 3 in top 3 are core)
        self.assertAlmostEqual(res['domain_precision'], 1.0)
        
        # Recall: Core features found: 3. Total core in definition: 6.
        # 3/6 = 0.5
        self.assertAlmostEqual(res['domain_recall'], 3/6)

    def test_precision_recall_mixed(self):
        # 1 Core (age), 1 Secondary (race), 1 Irrelevant (fnlwgt)
        feature_names = ['age', 'race', 'fnlwgt', 'random1', 'random2']
        
        weights = np.array([0.5, 0.4, 0.3, 0.0, 0.0])
        # Top 3: age, race, fnlwgt
        
        res = self.metric.compute(weights, feature_names, k=3)
        
        # Precision: 2/3 (age is Core, race is Secondary)
        self.assertAlmostEqual(res['domain_precision'], 2/3)
        
        # Recall: Found age (1). Total Core is 6.
        self.assertAlmostEqual(res['domain_recall'], 1/6)

    def test_one_hot_handling(self):
        # Features: occupation_Sales (Core), marital-status_Married (Secondary)
        feature_names = ['occupation_Sales', 'marital-status_Married-civ-spouse', 'fnlwgt']
        weights = np.array([0.9, 0.8, 0.1])
        
        res = self.metric.compute(weights, feature_names, k=2)
        
        # Top 2: occupation_Sales, marital-status...
        # Base names: occupation (Core), marital-status (Secondary)
        
        # Precision: 2/2 = 1.0
        self.assertAlmostEqual(res['domain_precision'], 1.0)
        
        # Recall: Found occupation (1). Total Core is 6.
        self.assertAlmostEqual(res['domain_recall'], 1/6)

if __name__ == '__main__':
    unittest.main()
