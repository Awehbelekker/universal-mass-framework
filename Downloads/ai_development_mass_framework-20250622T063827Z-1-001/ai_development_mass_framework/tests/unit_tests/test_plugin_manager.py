import unittest
from core.plugin_manager import PluginManager

class TestPluginManager(unittest.TestCase):
    def test_discover_plugins(self):
        pm = PluginManager('agents.research')
        pm.discover_plugins()
        self.assertIsInstance(pm.plugins, dict)

if __name__ == "__main__":
    unittest.main()
