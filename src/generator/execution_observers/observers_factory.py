from generator.execution_observers import PrintObserver
from generator.execution_observers.function import FunctionExecutionObserver
from generator.execution_observers.numeric_keypad import NumericKeypadExecutionObserver


class ObserversFactory(object):
    @staticmethod
    def make_stub():
        return PrintObserver()

    @staticmethod
    def make_numeric_keypad():
        return NumericKeypadExecutionObserver()

    @staticmethod
    def make_function():
        return FunctionExecutionObserver()

