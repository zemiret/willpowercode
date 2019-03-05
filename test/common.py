import os
import unittest

from generator import GeneratorStateMaster, Commander


class TestCase(unittest.TestCase):
    """
    Subclass this class for tests. It sets up required dependencies.
    """
    @classmethod
    def setUpClass(cls):
        gen = GeneratorStateMaster()
        gen.init('stub_screen')
        commander = Commander()
        commander.init(os.path.realpath(os.path.join(os.path.dirname(__file__), 'out', 'test.out')))
