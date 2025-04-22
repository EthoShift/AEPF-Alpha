import os
import importlib
import logging
from typing import List
from ethical_prisms.ethical_prism_agent import EthicalPrismAgent

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, plugins_dir: str = "plugins", create_if_missing: bool = False):
        self.plugins_dir = plugins_dir
        self.plugins: List[EthicalPrismAgent] = []
        self.create_if_missing = create_if_missing

    def load_plugins(self) -> None:
        """
        Discover and load plugins from the specified plugins directory.
        """
        if not os.path.isdir(self.plugins_dir):
            if self.create_if_missing:
                os.makedirs(self.plugins_dir)
                logger.info(f"Plugins directory '{self.plugins_dir}' created.")
            else:
                logger.warning(f"Plugins directory '{self.plugins_dir}' not found.")
                return

        for filename in os.listdir(self.plugins_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                module_name = filename[:-3]
                module_path = f"{self.plugins_dir}.{module_name}"
                try:
                    module = importlib.import_module(module_path)
                    if hasattr(module, "plugin"):
                        plugin_instance = getattr(module, "plugin")
                        if isinstance(plugin_instance, EthicalPrismAgent):
                            self.plugins.append(plugin_instance)
                            logger.info(f"Loaded plugin: {module_name}")
                        else:
                            logger.error(f"Plugin {module_name} does not implement EthicalPrismAgent.")
                    else:
                        logger.error(f"Module {module_name} does not define a 'plugin' instance.")
                except Exception as e:
                    logger.error(f"Failed to load plugin '{module_name}': {e}")

    def get_plugins(self) -> List[EthicalPrismAgent]:
        """
        Return the list of loaded plugins.
        """
        return self.plugins