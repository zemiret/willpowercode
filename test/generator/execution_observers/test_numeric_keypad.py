import unittest

from generator import GeneratorException
from generator.execution_observers.numeric_keypad import NumericKeypadExecutionObserver


class TestNumericKeypadExecutionObserver(unittest.TestCase):
    def setUp(self):
        self.observer = NumericKeypadExecutionObserver()

    def test_error_raising(self):
        with self.assertRaises(GeneratorException):
            self.observer.notify('123')
            self.observer.notify('10')
            self.observer.notify('-1')

    def test_correct_execution(self):
        try:
            for i in range(0, 10):
                self.observer.notify(str(i))
        except GeneratorException:
            self.fail('notify unexpectedly raised an exception!')
