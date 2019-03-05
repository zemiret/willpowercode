from generator import Commander, GeneratorError
from utils.common import abs_path

from .execution_observer import ExecutionObserver


class NumericKeypadExecutionObserver(ExecutionObserver):
    def __init__(self):
        def create_action(index):
            def _execute_action():
                Commander().append_command(
                    abs_path(__file__, '..', 'scripts', 'numeric_keypad', 'script' + str(index))
                )

            return _execute_action

        self._options = [create_action(i) for i in range(0, 10)]

    def notify(self, u_in: str):
        index = int(u_in)
        if index < 0:
            raise GeneratorError('Negative indexes are not allowed.')

        try:
            self._options[index]()
        except IndexError:
            raise GeneratorError('Not supported operation in NumericKeypadExecutionObserver.')
