import unittest
from core.persistent_memory import PersistentMemory
import os

class TestPersistentMemory(unittest.TestCase):
    def setUp(self):
        self.memory = PersistentMemory('test_memory.json')

    def tearDown(self):
        if os.path.exists('test_memory.json'):
            os.remove('test_memory.json')

    def test_set_and_get(self):
        self.memory.set('foo', 'bar')
        self.assertEqual(self.memory.get('foo'), 'bar')

if __name__ == "__main__":
    unittest.main()
