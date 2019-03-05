import unittest

from generator import Commander, GeneratorException
from generator.execution_observers.numeric_keypad import NumericKeypadExecutionObserver


class TestNumericKeypadExecutionObserver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Commander('stub_file')  # Init stub

    def setUp(self):
        self.observer = NumericKeypadExecutionObserver()

    def test_error_raising(self):
        self.assertRaises(GeneratorException, lambda: self.observer.notify('123'))
        self.assertRaises(GeneratorException, lambda: self.observer.notify('10'))
        self.assertRaises(GeneratorException, lambda: self.observer.notify('-1'))

    def test_correct_execution(self):
        try:
            for i in range(0, 10):
                self.observer.notify(str(i))
        except GeneratorException:
            self.fail('notify unexpectedly raised an exception!')
