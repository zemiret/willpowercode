from generator import WidgetsFactory
from generator.base import make_generator_entry
from generator.execution_observers.execution_observer import ExecutionObserver
from generator.execution_observers.observers_factory import ObserversFactory
from generator.widgets.common_gen import CommonWidget
from generator.widgets.navigation import NavigationWidget
from generator.widgets.refactor import RefactorWidget
from generator.widgets.write import WriteWidget
from . import GeneratorWidget


class TopLevelWidget(GeneratorWidget):
    @property
    def caption(self):
        return self._caption

    def __init__(self, execution_observer: ExecutionObserver = ObserversFactory.make_stub()):
        super().__init__(execution_observer)
        self._caption = 'Top level'

        self._options = {
            '0': make_generator_entry(WriteWidget.caption, WidgetsFactory.make_write()),
            '1': make_generator_entry(NavigationWidget.caption, WidgetsFactory.make_navigation()),
            '2': make_generator_entry(RefactorWidget.caption, WidgetsFactory.make_refactor()),
            '3': make_generator_entry(CommonWidget.caption, WidgetsFactory.make_common())
        }

    def display(self, screen):
        screen.clear()
        for i, (key, val) in enumerate(self._options.items()):
            screen.addstr(i, 0, key + ': ' + self._options[key]['caption'])
        screen.refresh()

    def handle_input(self, u_in):
        int_in = int(u_in)
        if not 0 <= int_in <= 3:
            return

        self._options[str(u_in)]['action']()
