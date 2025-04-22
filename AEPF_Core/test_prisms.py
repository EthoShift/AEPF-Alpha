import unittest
from typing import Dict, Any
from ethical_prisms.ecocentric import EcocentricPrism
from ethical_prisms.equity_focused import EquityFocusedPrism
from ethical_prisms.human_centric import HumanCentricPrism
from ethical_prisms.innovation_focused import InnovationFocusedPrism

class TestPrisms(unittest.TestCase):

    def test_ecocentric_prism(self):
        prism = EcocentricPrism()
        input_data = {
            'environmental_impact': 0.8,
            'biodiversity_preservation': 0.7,
            'carbon_neutrality': 0.9,
            'water_conservation': 0.6,
            'renewable_resource_use': 0.85
        }
        result = prism.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_equity_focused_prism(self):
        prism = EquityFocusedPrism()
        metrics = {
            'bias_mitigation_score': 0.8,
            'accessibility_score': 0.7,
            'representation_score': 0.9,
            'demographic_equity_score': 0.6,
            'resource_fairness_score': 0.75
        }
        result = prism.evaluate(metrics)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_human_centric_prism(self):
        prism = HumanCentricPrism()
        metrics = {
            'wellbeing_score': 0.8,
            'autonomy_score': 0.7,
            'privacy_score': 0.9,
            'transparency_score': 0.6,
            'accountability_score': 0.75,
            'fairness_score': 0.8,
            'safety_score': 0.85
        }
        result = prism.evaluate(metrics)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_innovation_focused_prism(self):
        prism = InnovationFocusedPrism()
        input_data = {
            'financial_risk': 0.2,
            'reputational_risk': 0.3,
            'technological_risk': 0.4,
            'economic_benefit': 0.9,
            'societal_benefit': 0.85
        }
        result = prism.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

if __name__ == '__main__':
    unittest.main() 