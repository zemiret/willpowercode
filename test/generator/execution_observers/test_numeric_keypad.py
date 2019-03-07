from generator.exceptions import GeneratorError
from generator.execution_observers.numeric_keypad import NumericKeypadExecutionObserver
from test.common import TestCase


class TestNumericKeypadExecutionObserver(TestCase):
    def setUp(self):
        self.observer = NumericKeypadExecutionObserver()

    def test_error_raising(self):
        self.assertRaises(GeneratorError, lambda: self.observer.notify('123'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('10'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('-1'))

    def test_correct_execution(self):
        try:
            for i in range(0, 10):
                self.observer.notify(str(i))
        except GeneratorError:
            self.fail('notify unexpectedly raised an exception!')
