import unittest
from typing import Dict, Any
from AEPF_Core.ethical_governor import EthicalGovernor
from AEPF_Core.plugin_manager import PluginManager
from AEPF_Core.action_controller import HostAIActionController
from ethical_prisms.ecocentric import EcocentricPrism

# Create a dummy HostAIActionController for testing
class DummyHostAIActionController(HostAIActionController):
    def __init__(self):
        self.called = False
        self.report_received = None

    def apply_decision(self, decision_report: Dict[str, Any]) -> None:
        self.called = True
        self.report_received = decision_report

# Optionally, override the ContextEngine to produce a synthetic scenario
class DummyContextEngine:
    def detect_scenario(self, input_data: Dict[str, Any]) -> str:
        return "synthetic_scenario"

class TestOutputReporting(unittest.TestCase):
    def setUp(self):
        # Initialize the Ethical Governor
        self.governor = EthicalGovernor()
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()

        # Create synthetic input data covering all necessary fields
        self.synthetic_input: Dict[str, Any] = {
            "human_centric": {"fairness_score": 0.8, "bias_reduction": 0.7},
            "equity_focused": {"equity_score": 0.9, "income_disparity": 0.4},
            "innovation_focused": {
                "tech_advancement": 0.85,
                "financial_risk": 0.3,
                "reputational_risk": 0.2,
                "technological_risk": 0.4,
                "economic_benefit": 0.75,
                "societal_benefit": 0.65
            },
            "ecocentric": {
                "carbon_footprint": 0.5,
                "environmental_impact": 0.6,
                "biodiversity_preservation": 0.7,
                "carbon_neutrality": 0.8,
                "water_conservation": 0.5,
                "renewable_resource_use": 0.8
            },
            "sentient_first": {
                "AI_ethics_score": 0.7,
                "sentient_welfare": 0.6,
                "empathy_score": 0.55,
                "autonomy_respect": 0.7,
                "sentient_safety": 0.8,
                "organisational_welfare": 0.9
            }
        }

        # Create a dummy HostAIActionController
        self.dummy_action_controller = DummyHostAIActionController()

        # Instantiate EthicalGovernor with a dummy ContextEngine and the dummy action controller
        self.ethical_governor = EthicalGovernor(action_controller=self.dummy_action_controller)
        self.ethical_governor.context_engine = DummyContextEngine()

    def test_output_format(self):
        # Define test input data
        test_input = {
            "ecocentric": {
                "carbon_footprint": 0.4,
                "environmental_impact": 0.5,
                "biodiversity_preservation": 0.6,
                "carbon_neutrality": 0.7,
                "water_conservation": 0.5,
                "renewable_resource_use": 0.8
            }
            # Add other prisms' data...
        }

        # Evaluate the input data
        result = self.governor.evaluate(test_input)

        # Check the output format
        self.assertIn("summary", result)
        self.assertIn("full_report", result)
        self.assertIn("prism_results", result["full_report"])

    def test_output_report_schema_and_action_invocation(self):
        # Evaluate using synthetic input data
        report = self.ethical_governor.evaluate(self.synthetic_input)

        # Verify that the output report has the required top-level keys
        self.assertIn("summary", report, "Output report missing 'summary'")
        self.assertIn("full_report", report, "Output report missing 'full_report'")

        # Check keys within the summary
        summary = report["summary"]
        for key in ["final_score", "scenario", "impact_predictions"]:
            self.assertIn(key, summary, f"'summary' missing '{key}'")

        # Check keys within the full_report
        full_report = report["full_report"]
        for key in ["prism_results", "weight_adjustments", "causal_analysis"]:
            self.assertIn(key, full_report, f"'full_report' missing '{key}'")

        # Verify that the dummy action controller was invoked with the report
        self.assertTrue(self.dummy_action_controller.called, "HostAIActionController.apply_decision was not called")
        self.assertEqual(self.dummy_action_controller.report_received, report, "Action controller received an incorrect report")

if __name__ == "__main__":
    unittest.main() 