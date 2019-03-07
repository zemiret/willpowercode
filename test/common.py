import os
import unittest

from generator import GeneratorStateMaster, Commander
from generator.buffers import GeneratorBuffers


class TestCase(unittest.TestCase):
    """
    Subclass this class for tests. It sets up required dependencies.
    """
    @classmethod
    def setUpClass(cls):
        buffers = GeneratorBuffers()

        gen = GeneratorStateMaster()
        gen.init('stub_screen', buffers)

        commander = Commander()
        commander.init(os.path.realpath(os.path.join(os.path.dirname(__file__), 'out', 'test.out')))
