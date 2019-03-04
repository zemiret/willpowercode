from generator import GeneratorStateMaster
from generator.widgets import GeneratorWidget


class TopLevelGeneratorWidget(GeneratorWidget):
    @property
    def caption(self):
        return self._caption

    def __init__(self):
        self._caption = 'Top level'
        master = GeneratorStateMaster()
        
        self._options = {
            '0': {
                'caption': NumericKeypad.caption,
                'action': lambda: master.append_state(NumericKeypad())
            },
            '1': {
                'caption': FunctionGeneratorWidget.caption,
                'action': lambda: master.append_state(FunctionGeneratorWidget())
            },
            '2': {
                'caption': StatementGenerator.caption,
                'action': lambda: master.append_state(StatementGenerator())
            },
            '3': {
                'caption': FunctionGeneratorWidget.caption,
                'action': lambda: master.append_state(FunctionGeneratorWidget())
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

