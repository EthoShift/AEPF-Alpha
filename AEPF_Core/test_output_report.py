import unittest
from AEPF_Core.ethical_governor import EthicalGovernor
from AEPF_Core.action_controller import HostAIActionController

class DummyActionController(HostAIActionController):
    def __init__(self):
        self.last_report = None

    def apply_decision(self, decision_report):
        self.last_report = decision_report

class TestOutputReport(unittest.TestCase):
    def test_output_report_schema(self):
        governor = EthicalGovernor()
        input_data = {"some_input": 1}
        report = governor.evaluate(input_data)
        self.assertIn("summary", report)
        self.assertIn("full_report", report)
        self.assertIn("final_score", report["summary"])
        self.assertIn("prism_results", report["full_report"])
        self.assertIn("weight_adjustments", report["full_report"])
        self.assertIn("causal_analysis", report["full_report"])

    def test_action_controller_integration(self):
        action_controller = DummyActionController()
        governor = EthicalGovernor(action_controller=action_controller)
        input_data = {"some_input": 1}
        report = governor.evaluate(input_data)
        self.assertEqual(action_controller.last_report, report)

if __name__ == "__main__":
    unittest.main() 