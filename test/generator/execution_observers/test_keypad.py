from generator.buffers import GeneratorBuffers
from generator.execution_observers.keypad import KeypadExecutionObserver
from test.common import TestCase


class TestKeypadExecutionObserver(TestCase):
    def setUp(self):
        self.observer = KeypadExecutionObserver()

    def test_write_to_buffer(self):
        self.observer.notify('kanapeczki')
        self.assertEqual(GeneratorBuffers().input.peek(), 'kanapeczki')

        self.observer.notify('abc123')
        self.assertEqual(GeneratorBuffers().input.peek(), 'kanapeczkiabc123')

        self.observer.notify('nope-and-nope')
        self.assertEqual(GeneratorBuffers().input.peek(), 'kanapeczkiabc123nope-and-nope')
