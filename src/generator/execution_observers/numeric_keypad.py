from generator import Commander
from utils.common import abs_path

from .execution_observer import ExecutionObserver


class GeneratorException(Exception):
    pass


class NumericKeypadExecutionObserver(ExecutionObserver):
    def __init__(self):
        self._options = [lambda:
                         Commander.append_command(abs_path(__file__, '..', 'scripts', 'numeric_keypad' + str(i)))
                         for i in range(0, 10)
                         ]

    def notify(self, u_in: str):
        try:
            self._options[int(u_in)]()
        except IndexError:
            raise GeneratorException()
