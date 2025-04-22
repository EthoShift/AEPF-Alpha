import unittest
from AEPF_Core.multi_agent_prism_system import MultiAgentPrismSystem
from AEPF_Core.ecocentric_agent import EcocentricAgent

class TestMultiAgentPrismSystem(unittest.TestCase):
    def setUp(self):
        # Initialize the system with the necessary agents
        self.system = MultiAgentPrismSystem(agents=[EcocentricAgent()])
        # Update synthetic input data to include all required keys
        self.sample_input = {
            "ecocentric": {
                "environmental_impact": 0.6,
                "biodiversity_preservation": 0.7,
                "carbon_neutrality": 0.8,
                "water_conservation": 0.5,
                "renewable_resource_use": 0.9
            }
        }

    def test_agent_evaluations(self):
        result = self.system.evaluate_all(self.sample_input)
        # Add assertions to verify the result
        self.assertIsNotNone(result)

    def test_aggregation_of_scores(self):
        result = self.system.evaluate_all(self.sample_input)
        # Add assertions to verify the result
        self.assertIsNotNone(result)
        self.assertIn('aggregated_score', result)
        self.assertIn('metrics', result)

    def test_handling_incomplete_input(self):
        incomplete_input = {
            "ecocentric": {
                "environmental_impact": 0.5,
                # Missing other keys
            }
        }
        with self.assertRaises(ValueError):
            self.system.evaluate_all(incomplete_input)

if __name__ == "__main__":
    unittest.main() 