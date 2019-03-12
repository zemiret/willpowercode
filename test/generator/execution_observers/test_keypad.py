from generator.exceptions import GeneratorError
from generator.execution_observers.keypad import KeypadExecutionObserver
from test.common import TestCase


class TestKeypadExecutionObserver(TestCase):
    def setUp(self):
        self.observer = KeypadExecutionObserver()

    def test_2digit_error_throwing(self):
        for i in range(100):
            self.assertRaises(GeneratorError, lambda: self.observer.notify(str(i)))

    def test_random_notify_out_of_range(self):
        self.assertRaises(GeneratorError, lambda: self.observer.notify('0000'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('0001'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('400'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('500'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('401'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('abc'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('333'))
        self.assertRaises(GeneratorError, lambda: self.observer.notify('322'))

    def test_correct_execution(self):
        try:
            self.notify_first_row()
            self.notify_from_2_row()
            self.notify_4option_keys()
            self.notify_additional_actions()

        except GeneratorError:
            self.fail('notify unexpectedly raised an exception!')

    def notify_first_row(self):
        self.observer.notify('000')
        self.observer.notify('001')
        self.observer.notify('002')

        self.observer.notify('010')
        self.observer.notify('011')
        self.observer.notify('012')

    def notify_from_2_row(self):
        for i in range(1, 2):
            for j in range(0, 2):
                for k in range(0, 2):
                    self.observer.notify(str(i) + str(j) + str(k))

    def notify_4option_keys(self):
        self.observer.notify('203')
        self.observer.notify('223')

    def notify_additional_actions(self):
        self.observer.notify('300')
