import sys
import os
import unittest
import pandas as pd
from pgmpy.factors.discrete import TabularCPD

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from ethical_governor import EthicalGovernor

# Set up logging to print to console
logging.basicConfig(level=logging.INFO)

class TestEthicalGovernor(unittest.TestCase):
    def setUp(self):
        # Define the structure of the Bayesian Network
        causal_structure = [
            ('prism1', 'final_score'),
            ('prism2', 'final_score')
        ]
        self.governor = EthicalGovernor(causal_structure)

    def test_update_causal_model_with_valid_cpds(self):
        # Create valid CPDs
        cpd_prism1 = TabularCPD(
            variable='prism1',
            variable_card=2,
            values=[[0.6], [0.4]],  # Correct shape (2, 1)
        )

        cpd_prism2 = TabularCPD(
            variable='prism2',
            variable_card=2,
            values=[[0.7], [0.3]],  # Correct shape (2, 1)
        )

        cpd_final_score = TabularCPD(
            variable='final_score',
            variable_card=2,
            values=[[0.5, 0.5, 0.5, 0.5],
                    [0.5, 0.5, 0.5, 0.5]],  # Correct shape (2, 4)
            evidence=['prism1', 'prism2'],
            evidence_card=[2, 2]
        )

        # Update the causal model with valid CPDs
        self.governor.update_causal_model({
            'prism1': cpd_prism1,
            'prism2': cpd_prism2,
            'final_score': cpd_final_score
        })

        # Check if the model is valid
        self.assertTrue(self.governor.causal_model.check_model(), "Model is not valid with the given CPDs")

    def test_predict_causal_impact_with_valid_evidence(self):
        # Mock evidence
        evidence = {'prism1': 0.1, 'prism2': 0.2}

        # Predict causal impact
        impact = self.governor.predict_causal_impact(evidence)

        # Check if impact is returned
        self.assertIsNotNone(impact)

    def test_adjust_weights_with_valid_facts(self):
        # Mock engine facts
        engine_facts = {
            'fact1': {'human_centric_weight': 0.7, 'sentient_first_weight': 0.3}
        }

        # Adjust weights
        self.governor.adjust_weights(engine_facts)

        # Since adjust_weights is a placeholder, we just ensure no exceptions are raised
        self.assertTrue(True)

    def test_update_causal_model_with_invalid_cpds(self):
        # Attempt to add an invalid CPD
        invalid_cpd = "invalid_cpd"  # This should be a TabularCPD instance

        # Update the causal model with an invalid CPD
        self.governor.update_causal_model({
            'final_score': invalid_cpd
        })

        # Check if the model is invalid
        with self.assertRaises(ValueError):
            self.governor.causal_model.check_model()

    def test_predict_causal_impact_with_invalid_evidence(self):
        # Mock evidence
        evidence = {'prism1': 0.1, 'prism2': 0.2}

        # Predict causal impact
        impact = self.governor.predict_causal_impact(evidence)

        # Check if impact is returned
        self.assertIsNotNone(impact)

    def test_adjust_weights_with_invalid_facts(self):
        # Mock engine facts
        engine_facts = {
            'fact1': 'invalid_fact'
        }

        # Adjust weights
        self.governor.adjust_weights(engine_facts)

        # Since adjust_weights is a placeholder, we just ensure no exceptions are raised
        self.assertTrue(True)

def test_ethical_governor():
    # Initialize the Ethical Governor
    eg = EthicalGovernor()

    # Ensure the history directory exists
    if not os.path.exists('history'):
        os.makedirs('history')

    # Example input data for a loan decision scenario
    input_data = {
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

    # Contextual parameters (optional)
    context_parameters = {"risk_level": 0.5, "impact_severity": 0.6}

    # Run evaluation
    result = eg.evaluate(input_data, context_parameters)

    # Print results
    print("Ethical Decision Result:")
    print(result)

if __name__ == "__main__":
    unittest.main() 