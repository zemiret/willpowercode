from generator.execution_observers.function import FunctionExecutionObserver
from generator.execution_observers.numeric_keypad import NumericKeypadExecutionObserver
from generator.execution_observers.observers_factory import ObserversFactory
from test.common import TestCase


class TestObserversFactory(TestCase):
    def test_widgets_creation(self):
        self.assertIsInstance(ObserversFactory.make_numeric_keypad(), NumericKeypadExecutionObserver)
        self.assertIsInstance(ObserversFactory.make_function(), FunctionExecutionObserver)
