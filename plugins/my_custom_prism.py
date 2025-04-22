from ethical_prisms.ethical_prism_agent import EthicalPrismAgent

class MyCustomPrism(EthicalPrismAgent):
    def evaluate(self, input_data: dict) -> dict:
        # Implement your evaluation logic here
        score = 0.95  # Example score calculation
        metrics = {"custom_metric": 0.8}  # Example metrics
        return {"score": score, "metrics": metrics}

# Export the plugin instance
plugin = MyCustomPrism() 