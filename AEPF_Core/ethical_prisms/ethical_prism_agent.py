from typing import Dict, Any
from abc import ABC, abstractmethod

class EthicalPrismAgent(ABC):
    @abstractmethod
    def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the ethical dimensions based on the given input data.

        Args:
            input_data (Dict[str, Any]): Input parameters for evaluation.

        Returns:
            Dict[str, Any]: A dictionary with keys 'score' (float) and 'metrics' (dict).
        """
        raise NotImplementedError("Subclasses must implement this method") 