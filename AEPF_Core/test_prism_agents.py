import unittest
from typing import Dict, Any
from ethical_prisms.ecocentric_prism_agent import EcocentricPrismAgent
from ethical_prisms.equity_focused_prism_agent import EquityFocusedPrismAgent
from ethical_prisms.human_centric_prism_agent import HumanCentricPrismAgent
from ethical_prisms.innovation_focused_prism_agent import InnovationFocusedPrismAgent
from ethical_prisms.sentient_first_prism_agent import SentientFirstPrismAgent

class TestPrismAgents(unittest.TestCase):

    def test_ecocentric_prism_agent(self):
        agent = EcocentricPrismAgent()
        input_data = {
            'carbon_footprint': 0.8,
            'environmental_impact': 0.7
        }
        result = agent.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_equity_focused_prism_agent(self):
        agent = EquityFocusedPrismAgent()
        input_data = {
            'bias_mitigation': 0.6,
            'equity_impact': 0.8
        }
        result = agent.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_human_centric_prism_agent(self):
        agent = HumanCentricPrismAgent()
        input_data = {
            'wellbeing': 0.9,
            'human_impact': 0.6
        }
        result = agent.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_innovation_focused_prism_agent(self):
        agent = InnovationFocusedPrismAgent()
        input_data = {
            'technological_advancement': 0.7,
            'innovation_impact': 0.9
        }
        result = agent.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

    def test_sentient_first_prism_agent(self):
        agent = SentientFirstPrismAgent()
        input_data = {
            'empathy': 0.85,
            'sentient_impact': 0.75
        }
        result = agent.evaluate(input_data)
        self.assertIn('score', result)
        self.assertIn('metrics', result)
        self.assertIsInstance(result['score'], float)

if __name__ == '__main__':
    unittest.main() 