from generator.exceptions import GeneratorError
from generator.base import make_pop_entry, make_execute_entry
from generator.execution_observers.execution_observer import ExecutionObserver
from . import GeneratorWidget


class NumericKeypadWidget(GeneratorWidget):
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
            '2': make_execute_entry(),
            '3': make_pop_entry(),
        }

    def display(self, screen, *args, **kwargs):
        if self._input_mode:
            self._display_options(screen, self.caption + ' - input', self._input_options)
        else:
            self._display_options(screen, self.caption, self._options)

    def _display_options(self, screen, caption: str, options):
        screen.addstr(0, 0, caption)
        for i, (key, val) in enumerate(options.items()):
            self._display_row(screen, i + 1, key, val)

    def _display_row(self, screen, index, key, value):
        screen.addstr(index, 0, key + ': ' + (value if type(value) is str else value['caption']))

    def handle_input(self, u_in):
        if not 0 <= int(u_in) <= 3:
            return

        try:
            self._handle_current_state_input(u_in)
        except KeyError:
            raise GeneratorError('Unsupported operation in NumericKeypadWidget.')

    def _handle_current_state_input(self, u_in):
        if self._input_mode:
            if len(self._cur_input) == 1:
                self._execution_observer.notify(NumericKeypadWidget._input_options[self._cur_input + u_in])
                self._cur_input = ''
                self._input_mode = False
            else:
                self._cur_input = u_in
        else:
            self._options[u_in]['action']()
