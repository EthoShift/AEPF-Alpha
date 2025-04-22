"""
Multi-Agent Prism System Documentation

Purpose:
The MultiAgentPrismSystem is designed to evaluate ethical considerations across multiple dimensions using a set of predefined prism agents. Each agent represents a different ethical perspective, such as ecocentric, equity-focused, human-centric, innovation-focused, and sentient-first. The system aggregates the scores from these agents to provide a comprehensive ethical decision score.

Adding a New Ethical Prism Agent:
1. Create a New Agent Class: Subclass the EthicalPrismAgent interface and implement the evaluate method.
2. Register the New Agent: Add the new agent to the MultiAgentPrismSystem class.

Configuring Weights for Score Aggregation:
- Default Weights: The system uses default weights if none are provided.
- Custom Weights: Pass a custom weights dictionary when instantiating the MultiAgentPrismSystem.

Running the Tests:
1. Ensure All Dependencies Are Installed.
2. Run the Tests: Navigate to the AEPF_Core directory and execute the test script using Python's unittest framework.
3. Check the Output: The test results will indicate whether the system is functioning as expected.
"""

from typing import Dict, Any, List
from AEPF_Core.ecocentric_agent import EcocentricAgent
from AEPF_Core.reinforcement_learning_manager import ReinforcementLearningManager

class MultiAgentPrismSystem:
    def __init__(self, rl_manager: ReinforcementLearningManager, agents: List[EcocentricAgent]):
        """
        Initialize the MultiAgentPrismSystem.

        Args:
            rl_manager (ReinforcementLearningManager): The RL manager to manage weights.
            agents (List[EcocentricAgent]): A list of ethical agents to evaluate input data.
        """
        self.rl_manager = rl_manager
        self.agents = agents

    def evaluate_all(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate input data using all agents and aggregate results using current weights.

        Args:
            input_data (Dict[str, Any]): The data to be evaluated.

        Returns:
            Dict[str, Any]: Aggregated evaluation results.
        """
        current_weights = self.rl_manager.get_current_weights()
        aggregated_score = 0.0
        metrics = {}

        for agent in self.agents:
            result = agent.evaluate(input_data)
            agent_name = type(agent).__name__
            score = result['score']
            aggregated_score += score * current_weights.get(agent_name, 0)
            metrics[agent_name] = result['metrics']

        return {"aggregated_score": aggregated_score, "metrics": metrics}

    def refine_system(self, evaluation_result: Dict[str, Any], reward: float) -> None:
        """
        Refine the system by updating the RL manager with the evaluation result and reward.

        Args:
            evaluation_result (Dict[str, Any]): The result from the evaluation.
            reward (float): The reward signal received from the environment/feedback.
        """
        self.rl_manager.update(evaluation_result, reward) 