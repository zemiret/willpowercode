from abc import abstractmethod

from generator.execution_observers.execution_observer import ExecutionObserver
from generator.widget_base import Widget


class GeneratorWidget(Widget):
    def __init__(self, execution_observer: ExecutionObserver):
        self._execution_observer = execution_observer
        self._options = {}

    @abstractmethod
    def display(self, screen, *args, **kwargs):
        """
        Default implementation for display method.
        Displays without caption (listing options from 1st line).
        To display caption call super from base class and then display caption.
        """
        screen.clear()
        for i, (key, val) in enumerate(self._options.items()):
            screen.addstr(i + 1, 0, key + ': ' + (val if type(val) is str else val['caption']))

    @abstractmethod
    def handle_input(self, u_in):
        pass
