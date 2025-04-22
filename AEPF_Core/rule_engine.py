from experta import *

class EthicalContext(Fact):
    """Information about the ethical context."""
    pass

class EthicalGovernorRules(KnowledgeEngine):
    @Rule(EthicalContext(bias_reduction=P(lambda x: x > 0.7), fairness_score=P(lambda x: x > 0.8)))
    def increase_human_centric_weight(self):
        print("Rule triggered: Increase human_centric weight")
        self.declare(Fact(human_centric_weight=1.1))

    @Rule(EthicalContext(sentient_welfare=P(lambda x: x < 0.5)))
    def decrease_sentient_first_weight(self):
        print("Rule triggered: Decrease sentient_first weight")
        self.declare(Fact(sentient_first_weight=0.9))

    # New Rule: Increase equity_focused weight if equity_score is high
    @Rule(EthicalContext(equity_score=P(lambda x: x > 0.8)))
    def increase_equity_focused_weight(self):
        print("Rule triggered: Increase equity_focused weight")
        self.declare(Fact(equity_focused_weight=1.2))

    # New Rule: Decrease innovation_focused weight if financial_risk is high
    @Rule(EthicalContext(financial_risk=P(lambda x: x > 0.7)))
    def decrease_innovation_focused_weight(self):
        print("Rule triggered: Decrease innovation_focused weight")
        self.declare(Fact(innovation_focused_weight=0.8))

    # New Rule: Increase ecocentric weight if carbon_footprint is low
    @Rule(EthicalContext(carbon_footprint=P(lambda x: x < 0.3)))
    def increase_ecocentric_weight(self):
        print("Rule triggered: Increase ecocentric weight")
        self.declare(Fact(ecocentric_weight=1.2))

    # Add more rules for other prisms as needed 