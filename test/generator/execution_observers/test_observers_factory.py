import unittest

from generator.execution_observers import NumericKeypadExecutionObserver
from generator.execution_observers.observers_factory import ObserversFactory


class TestObserversFactory(unittest.TestCase):
    def test_widgets_creation(self):
        self.assertIsInstance(ObserversFactory.make_numeric_keypad(), NumericKeypadExecutionObserver)


if __name__ == '__main__':
    unittest.main()
