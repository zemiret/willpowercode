from generator.execution_observers import NumericKeypadExecutionObserver, FunctionExecutionObserver
from generator.execution_observers.observers_factory import ObserversFactory
from test.common import TestCase


class TestObserversFactory(TestCase):
    def test_widgets_creation(self):
        self.assertIsInstance(ObserversFactory.make_numeric_keypad(), NumericKeypadExecutionObserver)
        self.assertIsInstance(ObserversFactory.make_function(), FunctionExecutionObserver)


if __name__ == '__main__':
    unittest.main()
