import unittest
from AEPF_Core.reinforcement_learning_manager import ReinforcementLearningManager

class TestReinforcementLearningManager(unittest.TestCase):
    def setUp(self):
        initial_weights = {
            "ecocentric": 0.2,
            "equity_focused": 0.2,
            "human_centric": 0.2,
            "innovation_focused": 0.2,
            "sentient_first": 0.2
        }
        self.rl_manager = ReinforcementLearningManager(initial_weights, learning_rate=0.1, epsilon=0.1)

    def test_select_action_weights_sum_to_one(self):
        updated_weights = self.rl_manager.select_action()
        total_weight = sum(updated_weights.values())
        self.assertAlmostEqual(total_weight, 1.0, places=5, msg="Weights do not sum to 1")

    def test_update_adjusts_weights(self):
        initial_weights = self.rl_manager.get_current_weights().copy()
        decision_result = {}  # Mock decision result
        reward = 0.5  # Example reward
        self.rl_manager.update(decision_result, reward)
        updated_weights = self.rl_manager.get_current_weights()

        # Check that the updated weights differ from the initial weights
        self.assertNotEqual(initial_weights, updated_weights, "Weights did not change after update")

    def test_update_with_no_reward(self):
        initial_weights = self.rl_manager.get_current_weights().copy()
        decision_result = {}  # Mock decision result
        reward = 0.0  # No reward
        self.rl_manager.update(decision_result, reward)
        updated_weights = self.rl_manager.get_current_weights()

        # Check that the updated weights differ from the initial weights
        self.assertNotEqual(initial_weights, updated_weights, "Weights did not change after update with no reward")

if __name__ == '__main__':
    unittest.main() 