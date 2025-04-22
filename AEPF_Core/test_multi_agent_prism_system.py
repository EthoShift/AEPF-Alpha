import unittest
from multi_agent_prism_system import MultiAgentPrismSystem
from reinforcement_learning_manager import ReinforcementLearningManager
from ethical_prisms.ecocentric import EcocentricPrism

class TestMultiAgentPrismSystem(unittest.TestCase):
    def setUp(self):
        # Create mock objects or use real instances as needed
        rl_manager = ReinforcementLearningManager(initial_weights={"ecocentric": 0.2, "equity_focused": 0.2, "human_centric": 0.2, "innovation_focused": 0.2, "sentient_first": 0.2})
        agents = [EcocentricPrism()]  # Add other agents as needed
        self.system = MultiAgentPrismSystem(rl_manager=rl_manager, agents=agents)
        self.sample_input = {
            "ecocentric": {"carbon_footprint": 0.4, "environmental_impact": 0.5},
            "equity_focused": {"bias_mitigation": 0.3, "equity_impact": 0.6},
            "human_centric": {"wellbeing": 0.8, "human_impact": 0.7},
            "innovation_focused": {"technological_advancement": 0.9, "innovation_impact": 0.8},
            "sentient_first": {"empathy": 0.7, "sentient_impact": 0.6},
        }

    def test_agent_evaluations(self):
        result = self.system.evaluate_all(self.sample_input)
        self.assertIn("final_score", result)
        self.assertIn("detailed_report", result)
        for agent in self.system.agents:
            self.assertIn(agent, result["detailed_report"])
            self.assertIn("score", result["detailed_report"][agent])
            self.assertIn("metrics", result["detailed_report"][agent])

    def test_aggregation_of_scores(self):
        result = self.system.evaluate_all(self.sample_input)
        expected_final_score = sum(
            self.system.weights[agent] * result["detailed_report"][agent]["score"]
            for agent in self.system.agents
        )
        self.assertAlmostEqual(result["final_score"], expected_final_score, places=5)

    def test_handling_incomplete_input(self):
        incomplete_input = {
            "ecocentric": {"carbon_footprint": 0.4},
            "equity_focused": {},
            "human_centric": {"wellbeing": 0.8},
            "innovation_focused": {"technological_advancement": 0.9},
            "sentient_first": {},
        }
        result = self.system.evaluate_all(incomplete_input)
        self.assertIn("final_score", result)
        self.assertIn("detailed_report", result)
        for agent in self.system.agents:
            self.assertIn(agent, result["detailed_report"])
            self.assertIn("score", result["detailed_report"][agent])
            self.assertIn("metrics", result["detailed_report"][agent])

if __name__ == "__main__":
    unittest.main() 