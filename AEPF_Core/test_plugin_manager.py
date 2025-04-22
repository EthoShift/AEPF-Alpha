import unittest
import os
import shutil
from AEPF_Core.plugin_manager import PluginManager
from ethical_prisms.ethical_prism_agent import EthicalPrismAgent

# Dummy plugin for testing
dummy_plugin_code = """
from ethical_prisms.ethical_prism_agent import EthicalPrismAgent

class DummyPrism(EthicalPrismAgent):
    def evaluate(self, input_data: dict) -> dict:
        return {"score": 0.5, "metrics": {"dummy": True}}

plugin = DummyPrism()
"""

# Invalid plugin for testing
invalid_plugin_code = """
class InvalidPrism:
    def evaluate(self, input_data: dict) -> dict:
        return {"score": 0.5, "metrics": {"invalid": True}}
"""

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary plugins directory
        self.plugins_dir = "test_plugins"
        os.makedirs(self.plugins_dir, exist_ok=True)

        # Create a valid dummy plugin
        with open(os.path.join(self.plugins_dir, "dummy_plugin.py"), "w") as f:
            f.write(dummy_plugin_code)

        # Create an invalid plugin
        with open(os.path.join(self.plugins_dir, "invalid_plugin.py"), "w") as f:
            f.write(invalid_plugin_code)

    def tearDown(self):
        # Remove the temporary plugins directory
        shutil.rmtree(self.plugins_dir)

    def test_load_valid_plugin(self):
        manager = PluginManager(plugins_dir=self.plugins_dir)
        manager.load_plugins()
        plugins = manager.get_plugins()
        self.assertEqual(len(plugins), 1)
        self.assertIsInstance(plugins[0], EthicalPrismAgent)

    def test_ignore_invalid_plugin(self):
        manager = PluginManager(plugins_dir=self.plugins_dir)
        manager.load_plugins()
        plugins = manager.get_plugins()
        self.assertEqual(len(plugins), 1)  # Only the valid plugin should be loaded

if __name__ == "__main__":
    unittest.main() 