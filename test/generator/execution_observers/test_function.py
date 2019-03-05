from generator import GeneratorError
from generator.execution_observers import FunctionExecutionObserver
from test.common import TestCase


class TestFunctionExecutionObserver(TestCase):
    def setUp(self):
        self.observer = FunctionExecutionObserver()

    def test_error_raising(self):
        self.assertRaises(GeneratorError, lambda: self.observer.notify('123'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('10'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('-1'))

    def test_correct_execution(self):
        try:
            for i in range(0, 3):
                self.observer.notify(str(i))
        except GeneratorError:
            self.fail('notify unexpectedly raised an exception!')
