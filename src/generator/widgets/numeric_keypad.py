from generator import GeneratorStateMaster, Commander
from generator.execution_observers.execution_observer import ExecutionObserver
from . import GeneratorWidget


class NumericKeypadGeneratorWidget(GeneratorWidget):
    caption = 'Numeric keypad'

    _input_options = {
        '00': '0',
        '01': '1',
        '02': '2',
        '03': '3',
        '10': '4',
        '11': '5',
        '12': '6',
        '13': '7',
        '20': '8',
        '21': '9',
    }

    def __init__(self, execution_observer: ExecutionObserver):
        super().__init__(execution_observer)
        self.result = []
        self._cur_input = ''
        self._input_mode = False

        master = GeneratorStateMaster()

        def _set_input_mode_action(input_mode):
            def set_input_mode():
                self._input_mode = input_mode

            return set_input_mode

        self._options = {
            '0': {
                'caption': 'input',
                'action': _set_input_mode_action(True)
            },
            '1': {
                'caption': 'delete last',
                'action': lambda: len(self.result) > 0 and self.result.pop()
            },
            '2': {
                'caption': 'accept',
                'action': lambda: Commander().execute()
            },
            '3': {
                'caption': 'back',
                'action': lambda: master.pop_state()
            }
        }

    def reset(self):
        pass

    def _display_input_mode(self, screen):
        screen.clear()
        screen.addstr(0, 0, self.caption + ' - input')
        for i, (key, val) in enumerate(self._input_options.items()):
            screen.addstr(i + 1, 0, key + ': ' + val['caption'])
        screen.refresh()

    def _display_options(self, screen):
        screen.clear()
        screen.addstr(0, 0, self.caption)
        for i, (key, val) in enumerate(self._options.items()):
            screen.addstr(i + 1, 0, key + ': ' + val['caption'])
        screen.refresh()

    def display(self, screen):
        if self._input_mode:
            self._display_input_mode(screen)
        else:
            self._display_options(screen)

    def handle_input(self, u_in):
        if not 0 <= int(u_in) <= 3:
            return

        if self._input_mode:
            if len(self._cur_input) == 1:
                self._execution_observer.notify(NumericKeypadGeneratorWidget._input_options[self._cur_input + u_in])
                self._cur_input = ''
                self._input_mode = False
            else:
                self._cur_input = u_in
        else:
            self._options[u_in]['action']()
