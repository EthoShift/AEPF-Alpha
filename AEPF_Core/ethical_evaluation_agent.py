from abc import ABC, abstractmethod
from typing import Dict, Any

class IEthicalAgent(ABC):
    @abstractmethod
    def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the input data using ethical principles.

        Args:
            input_data (Dict[str, Any]): The data to be evaluated.

        Returns:
            Dict[str, Any]: A dictionary containing evaluation results, 
                            including keys such as 'score' and 'metrics'.
        """
        pass

# Example implementation of the interface
class ExampleEthicalAgent(IEthicalAgent):
    def evaluate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement specific ethical evaluation logic
        return {"decision": "approved", "score": 0.85, "metrics": {"consistency": 0.9}} 