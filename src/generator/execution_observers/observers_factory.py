from generator.execution_observers import PrintObserver, NumericKeypadExecutionObserver


class ObserversFactory(object):
    @staticmethod
    def make_stub():
        return PrintObserver()

    @staticmethod
    def make_numeric_keypad():
        return NumericKeypadExecutionObserver()
