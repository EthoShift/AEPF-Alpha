from typing import Dict, Any, List
import logging
import pickle
from datetime import datetime
from pathlib import Path
import numpy as np
import networkx as nx
from causalnex.structure.notears import from_pandas
from causalnex.inference import InferenceEngine
from causalnex.structure import StructureModel
from causalnex.network import BayesianNetwork
from causalnex.plots import plot_structure
from ethical_prisms.ecocentric import EcocentricPrism
from ethical_prisms.equity_focused import EquityFocusedPrism
from ethical_prisms.human_centric import HumanCentricPrism
from ethical_prisms.innovation_focused import InnovationFocusedPrism
from ethical_prisms.sentient_first import SentientFirstPrism
from Context_manager import ContextEngine
import os
from rule_engine import EthicalGovernorRules, EthicalContext
import pandas as pd  # Ensure pandas is imported
from pgmpy.models import BayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.factors.discrete import TabularCPD
from plugin_manager import PluginManager
from action_controller import HostAIActionController

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EthicalGovernor:
    def __init__(self, causal_structure: List[tuple] = None, action_controller: HostAIActionController = None):
        """
        Initialize the Ethical Governor with a configurable causal structure.

        Args:
            causal_structure (List[tuple], optional): List of edges defining the Bayesian network structure.
            action_controller: The action controller for applying decisions to the host AI.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.prisms = {
            "ecocentric": EcocentricPrism(),
            "equity_focused": EquityFocusedPrism(),
            "human_centric": HumanCentricPrism(),
            "innovation_focused": InnovationFocusedPrism(),
            "sentient_first": SentientFirstPrism()
        }
        self.context_engine = ContextEngine()
        self.history_path = Path("history/ethical_governor_history.pkl")
        self.causal_model_path = Path("models/causal_model.pkl")
        self.decision_history = self.load_history()
        self.causal_model = BayesianNetwork(causal_structure or [])
        self.inference = None  # Delay inference initialization
        self.action_controller = action_controller
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
    
    def load_history(self):
        if self.history_path.exists():
            with open(self.history_path, "rb") as f:
                return pickle.load(f)
        return []
    
    def save_history(self):
        with open(self.history_path, "wb") as f:
            pickle.dump(self.decision_history, f)
    
    def load_causal_model(self):
        if self.causal_model_path.exists():
            with open(self.causal_model_path, "rb") as f:
                self.logger.info("Loading causal model from file.")
                return pickle.load(f)
        self.logger.warning("Causal model file not found.")
        return None
    
    def _is_valid_cpd(self, cpd: TabularCPD, expected_parents: set) -> bool:
        # Type Check
        if not isinstance(cpd, TabularCPD):
            self.logger.warning("Provided CPD is not a TabularCPD.")
            return False

        # Parent Check
        cpd_parents = set(cpd.get_evidence())
        if cpd_parents != expected_parents:
            self.logger.warning(f"CPD for {cpd.variable} has mismatched parents. Expected: {expected_parents}, Found: {cpd_parents}")
            return False

        return True

    def update_causal_model(self, cpds: Dict[str, TabularCPD]):
        """
        Update the causal model with the provided CPDs.

        Args:
            cpds (Dict[str, TabularCPD]): Conditional Probability Distributions for the model.
        """
        for node, cpd in cpds.items():
            expected_parents = set(self.causal_model.get_parents(node))
            if self._is_valid_cpd(cpd, expected_parents):
                self.causal_model.add_cpds(cpd)
            else:
                self.logger.error(f"Invalid CPD for {node}. It will not be added to the model.")

        # Initialize inference after adding CPDs
        try:
            self.causal_model.check_model()
            self.inference = VariableElimination(self.causal_model)
        except Exception as e:
            self.logger.error(f"Failed to initialize inference: {e}")
    
    def predict_causal_impact(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Predict the causal impact based on the given evidence.

        Args:
            evidence (Dict[str, Any]): Evidence for the Bayesian inference.

        Returns:
            Dict[str, Any]: Predicted impact on the final score.
        """
        if not self.inference:
            self.logger.error("Inference not initialized. Ensure CPDs are added before prediction.")
            return {"error": "Causal model not available."}

        try:
            query_result = self.inference.query(variables=['final_score'], evidence=evidence)
            return query_result.values
        except Exception as e:
            self.logger.error(f"Failed to predict causal impact: {e}")
            return {}

    def adjust_weights(self, engine_facts: Dict[str, Any]):
        """
        Adjust weights based on the rule engine's facts.

        Args:
            engine_facts (Dict[str, Any]): Facts from the rule engine.
        """
        for fact in engine_facts.values():
            if not isinstance(fact, dict):
                self.logger.error("Fact is not structured as a dictionary.")
                continue
            # Process valid fact
            try:
                human_centric_weight = fact.get("human_centric_weight", 0)
                sentient_first_weight = fact.get("sentient_first_weight", 0)
            except KeyError as e:
                self.logger.warning(f"Missing expected key in fact: {e}")

    def normalize_weights(self, weights: Dict[str, float]) -> Dict[str, float]:
        """
        Normalize the weights to ensure they sum to 1.

        Args:
            weights (Dict[str, float]): The weights to be normalized.

        Returns:
            Dict[str, float]: Normalized weights.
        """
        total_weight = sum(weights.values())
        if total_weight == 0:
            self.logger.warning("Total weight is zero. Adjusting to equal distribution.")
            num_weights = len(weights)
            return {k: 1.0 / num_weights for k in weights}
        return {k: v / total_weight for k, v in weights.items()}

    def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the input data and context parameters to produce a decision.

        Args:
            input_data (Dict): The input data for evaluation.

        Returns:
            Dict: Evaluation results including final score and impact predictions.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        scenario = self.context_engine.detect_scenario(input_data)
        
        # Initialize the rule engine
        engine = EthicalGovernorRules()
        engine.reset()
        
        # Insert facts into the rule engine
        engine.declare(EthicalContext(**input_data))
        
        # Run the rule engine
        engine.run()
        
        # Collect results from the rule engine
        weights = {
            'equity_focused': 0.3,
            'human_centric': 0.3,
            'innovation_focused': 0.15,
            'ecocentric': 0.15,
            'sentient_first': 0.1
        }
        
        # Normalize weights
        weights = self.normalize_weights(weights)
        
        # Continue with the existing evaluation logic
        prism_results = {}
        for plugin in self.plugin_manager.get_plugins():
            result = plugin.evaluate(input_data)
            prism_results[plugin.__class__.__name__] = result
        
        print("Prism Results:", prism_results)
        
        total_score = sum(weights[p] * prism_results[p]['score'] for p in prism_results if p in weights) / sum(weights.values())
        
        self.decision_history.append({
            'timestamp': timestamp,
            'scenario': scenario,
            'weights': weights,
            'prism_results': prism_results,
            'total_score': total_score
        })
        self.save_history()
        
        impact_predictions = self.predict_causal_impact(prism_results)
        
        report = {
            'summary': {
                'final_score': total_score,
                'scenario': scenario,
                'impact_predictions': impact_predictions
            },
            'full_report': {
                'prism_results': prism_results,
                'weight_adjustments': weights,
                'causal_analysis': impact_predictions
            }
        }

        if self.action_controller:
            try:
                self.action_controller.apply_decision(report)
            except Exception as e:
                self.logger.error(f"Failed to apply ethical decision to host AI: {e}")

        return report

    def process_facts(self, facts: List[Any]) -> List[Dict[str, Any]]:
        processed_facts = []
        for fact in facts:
            if isinstance(fact, dict):
                processed_facts.append(fact)
            else:
                self.logger.error("Fact is not structured as a dictionary.")
                self.logger.warning("Skipping invalid fact.")
                # Optionally, add a default fact or take other corrective action
                # processed_facts.append(self._default_fact())

        return processed_facts

    def _generate_report(self, facts: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Generate a report based on valid facts
        # ...
        report = {
            "summary": {
                "final_score": 0.0,  # Example placeholder
                "scenario": "example_scenario",
                "impact_predictions": {}
            },
            "full_report": {
                "prism_results": {},
                "weight_adjustments": {},
                "causal_analysis": {}
            }
        }
        return report

def test_ethical_governor():
    # Initialize the Ethical Governor with a sample causal structure
    causal_structure = [
        ('human_centric', 'final_score'),
        ('equity_focused', 'final_score'),
        ('innovation_focused', 'final_score'),
        ('ecocentric', 'final_score'),
        ('sentient_first', 'final_score')
    ]
    eg = EthicalGovernor(causal_structure)

    # Define test input data
    test_input = {
        "human_centric": {"fairness_score": 0.7, "bias_reduction": 0.6},
        "equity_focused": {"equity_score": 0.8, "income_disparity": 0.5},
        "innovation_focused": {
            "tech_advancement": 0.9,
            "financial_risk": 0.3,
            "reputational_risk": 0.2,
            "technological_risk": 0.4,
            "economic_benefit": 0.7,
            "societal_benefit": 0.6
        },
        "ecocentric": {
            "carbon_footprint": 0.4,
            "environmental_impact": 0.5,
            "biodiversity_preservation": 0.6,
            "carbon_neutrality": 0.7,
            "water_conservation": 0.5,
            "renewable_resource_use": 0.8
        },
        "sentient_first": {
            "AI_ethics_score": 0.7,
            "sentient_welfare": 0.6,
            "empathy_score": 0.5,
            "autonomy_respect": 0.7,
            "sentient_safety": 0.8,
            "organisational_welfare": 0.9
        }
    }
    context_params = {"risk_level": 0.5, "impact_severity": 0.6}

    # Manually update the causal model with a valid DataFrame
    # This is a placeholder for actual CPD updates
    # eg.update_causal_model(pd.DataFrame([test_input]))

    # Evaluate the input data
    result = eg.evaluate(test_input)

    # Print the result
    print(result)

def run_evaluations(input_data: Dict[str, Any]) -> Dict[str, Any]:
    plugin_manager = PluginManager()
    plugin_manager.load_plugins()
    results = {}
    for plugin in plugin_manager.get_plugins():
        result = plugin.evaluate(input_data)
        results[plugin.__class__.__name__] = result
    # Aggregate and format results as needed
    return results

if __name__ == "__main__":
    test_ethical_governor()
