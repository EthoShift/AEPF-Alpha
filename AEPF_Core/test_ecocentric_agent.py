import unittest
import sys
import os

# Add the root directory to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ethical_governor import EthicalGovernor
from pgmpy.factors.discrete import TabularCPD

class TestEcocentricAgent(unittest.TestCase):
    def setUp(self):
        # Define the structure of the Bayesian Network
        causal_structure = [
            ('prism1', 'final_score'),
            ('prism2', 'final_score')
        ]
        self.governor = EthicalGovernor(causal_structure)

        # Update synthetic input data to include all required keys
        self.synthetic_input = {
            "ecocentric": {
                "environmental_impact": 0.5,
                "biodiversity_preservation": 0.6,
                "carbon_neutrality": 0.7,
                "water_conservation": 0.8,
                "renewable_resource_use": 0.9
            }
        }

    def test_valid_cpds(self):
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

if __name__ == "__main__":
    unittest.main() 