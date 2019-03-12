from generator.base import COMMON_CAPTIONS
from generator.execution_observers import ExecutionObserver
from . import GeneratorWidget


class FunctionWidget(GeneratorWidget):
    caption = 'Functions'

    def __init__(self, execution_observer: ExecutionObserver):
        super().__init__(execution_observer)
        self._options = {
            '0': 'Decorator',
            '1': 'Function',
            '2': COMMON_CAPTIONS['back'],
        }

    def display(self, screen, *args, **kwargs):
        super().display(screen)
        screen.addstr(0, 0, FunctionWidget.caption)

    def handle_input(self, u_in):
        self._execution_observer.notify(u_in)
