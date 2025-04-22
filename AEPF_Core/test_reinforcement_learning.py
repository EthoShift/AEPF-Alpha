import unittest
from reinforcement_learning import ReinforcementLearningManager

class TestReinforcementLearningManager(unittest.TestCase):
    def setUp(self):
        initial_weights = {
            "ecocentric": 0.2,
            "equity_focused": 0.2,
            "human_centric": 0.2,
            "innovation_focused": 0.2,
            "sentient_first": 0.2,
        }
        self.rl_manager = ReinforcementLearningManager(initial_weights)

    def test_weight_update(self):
        decision_result = {"final_score": 0.5, "detailed_report": {}}
        initial_weights = self.rl_manager.get_current_weights().copy()
        self.rl_manager.update(decision_result, reward=1.0)
        updated_weights = self.rl_manager.get_current_weights()
        self.assertNotEqual(initial_weights, updated_weights)

    def test_epsilon_greedy(self):
        initial_weights = self.rl_manager.get_current_weights().copy()
        for _ in range(100):
            self.rl_manager.select_action()
        updated_weights = self.rl_manager.get_current_weights()
        self.assertNotEqual(initial_weights, updated_weights)

if __name__ == "__main__":
    unittest.main() 