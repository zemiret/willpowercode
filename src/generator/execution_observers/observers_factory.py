from generator.execution_observers import FunctionExecutionObserver, NumericKeypadExecutionObserver, PrintObserver


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

