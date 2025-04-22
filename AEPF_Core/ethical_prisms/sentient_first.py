import logging
from ethical_prisms.ethical_prism_agent import EthicalPrismAgent

class SentientFirstPrism(EthicalPrismAgent):
    def __init__(self):
        self.prism_name = "Sentient-First"
        self.logger = logging.getLogger(self.__class__.__name__)

    def evaluate(self, input_data):
        """
        Evaluate the sentient-first prism with provided input data.

        Args:
            input_data (dict): Input data containing scores for evaluation.

        Returns:
            dict: Evaluated metrics and their narratives.
        """
        self.logger.debug(f"Evaluating {self.prism_name} with input: {input_data}")
        required_inputs = [
            "sentient_welfare",
            "empathy_score",
            "autonomy_respect",
            "sentient_safety",
            "organisational_welfare"
        ]

        # Validate input data
        for key in required_inputs:
            if key not in input_data:
                self.logger.error(f"Missing required input data: {key}")
                raise ValueError(f"Missing required input data: {key}")
            if not isinstance(input_data[key], (int, float)) or not (0 <= input_data[key] <= 1):
                self.logger.error(f"{key} must be a numeric value between 0 and 1.")
                raise ValueError(f"{key} must be a numeric value between 0 and 1.")

        # Process metrics
        metrics = {
            "sentient_welfare": {
                "value": input_data["sentient_welfare"],
                "narrative": f"Sentient welfare score directly input as {input_data['sentient_welfare']:.2f}."
            },
            "empathy_score": {
                "value": input_data["empathy_score"],
                "narrative": f"Empathy score for sentient beings is {input_data['empathy_score']:.2f}."
            },
            "autonomy_respect": {
                "value": input_data["autonomy_respect"],
                "narrative": f"Respect for autonomy of sentient beings is {input_data['autonomy_respect']:.2f}."
            },
            "sentient_safety": {
                "value": input_data["sentient_safety"],
                "narrative": f"Sentient safety measures score is {input_data['sentient_safety']:.2f}."
            },
            "organisational_welfare": {
                "value": input_data["organisational_welfare"],
                "narrative": f"Organisational welfare impact score is {input_data['organisational_welfare']:.2f}."
            },
        }

        # Calculate the score
        score = self.calculate_score(input_data)
        self.logger.info(f"Calculated score: {score}")

        # Return structured output
        return {
            "prism": self.prism_name,
            "metrics": metrics,
            "score": score
        }

    def calculate_score(self, input_data):
        self.logger.debug(f"Calculating score for {self.prism_name} with input: {input_data}")
        try:
            score = (input_data['AI_ethics_score'] + input_data['sentient_welfare'] +
                     input_data['empathy_score'] + input_data['autonomy_respect'] +
                     input_data['sentient_safety'] + input_data['organisational_welfare']) / 6
            self.logger.info(f"Calculated score: {score}")
            return score
        except KeyError as e:
            self.logger.error(f"Missing key in input data: {e}")
            return 0.0
