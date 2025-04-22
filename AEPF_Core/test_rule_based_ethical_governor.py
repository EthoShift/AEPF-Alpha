import os
from ethical_governor import EthicalGovernor

def test_rule_based_ethical_governor():
    # Initialize the Ethical Governor
    eg = EthicalGovernor()

    # Ensure the history directory exists
    if not os.path.exists('history'):
        os.makedirs('history')

    # Example input data for a decision scenario
    input_data = {
        "human_centric": {"fairness_score": 0.85, "bias_reduction": 0.75},
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
            "sentient_welfare": 0.4,  # This should trigger a rule
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
    test_rule_based_ethical_governor() 