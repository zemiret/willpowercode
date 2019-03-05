from generator import WidgetsFactory, GeneratorStateMaster
from generator.execution_observers.execution_observer import ExecutionObserver
from generator.widgets.function import FunctionGeneratorWidget
from generator.widgets.numeric_keypad import NumericKeypadGeneratorWidget
from generator.widgets.statement import StatementGeneratorWidget
from . import GeneratorWidget


class TopLevelGeneratorWidget(GeneratorWidget):
    @property
    def caption(self):
        return self._caption

    def __init__(self, execution_observer: ExecutionObserver):
        super().__init__(execution_observer)
        self._caption = 'Top level'
        master = GeneratorStateMaster()
        
        self._options = {
            '0': {
                'caption': NumericKeypadGeneratorWidget.caption,
                'action': lambda: master.append_state(WidgetsFactory.make_numeric_keypad())
            },
            '1': {
                'caption': FunctionGeneratorWidget.caption,
                'action': lambda: master.append_state(WidgetsFactory.make_function())
            },
            '2': {
                'caption': StatementGeneratorWidget.caption,
                'action': lambda: master.append_state(WidgetsFactory.make_statement())
            },
            '3': {
                'caption': FunctionGeneratorWidget.caption,
                'action': lambda: master.append_state(WidgetsFactory.make_function())
            },
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

    def reset(self):
        pass
