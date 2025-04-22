import os
import pandas as pd
import logging
from ethical_governor import EthicalGovernor

logger = logging.getLogger(__name__)

def create_and_save_causal_model():
    try:
        # Initialize the Ethical Governor
        eg = EthicalGovernor()

        # Ensure the models directory exists
        models_dir = os.path.dirname(eg.causal_model_path)
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        # Example data to fit the Bayesian Network
        # Replace this with your actual data
        data = pd.DataFrame({
            "human_centric": [0.7, 0.8, 0.6],
            "sentient_first": [0.5, 0.6, 0.4],
            "ecocentric": [0.4, 0.5, 0.3],
            "innovation_focused": [0.6, 0.7, 0.5],
            "equity_focused": [0.8, 0.9, 0.7],
            "final_score": [0.75, 0.85, 0.65]
        })

        # Update and save the causal model
        eg.update_causal_model(data)
        logger.info("Causal model updated and saved successfully.")

    except Exception as e:
        logger.error(f"Failed to create and save causal model: {e}")

if __name__ == "__main__":
    create_and_save_causal_model() 