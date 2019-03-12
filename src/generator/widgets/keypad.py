from generator import GeneratorStateMaster
from generator.exceptions import GeneratorError
from generator.widgets import GeneratorWidget


class KeypadWidget(GeneratorWidget):
    caption = 'Keypad'

    def __init__(self, observer):
        super().__init__(observer)

        self.current_option_code = ''
        self._internal_buffer = ''

        self._options = {
            '00': {
                '0': 'a',
                '1': 'b',
                '2': 'c',
            },
            '01': {
                '0': 'd',
                '1': 'e',
                '2': 'f',
            },
            '10': {
                '0': 'g',
                '1': 'h',
                '2': 'i',
            },
            '11': {
                '0': 'j',
                '1': 'k',
                '2': 'l',
            },
            '12': {
                '0': 'm',
                '1': 'n',
                '2': 'o',
            },
            '20': {
                '0': 'p',
                '1': 'q',
                '2': 'r',
                '3': 's',
            },
            '21': {
                '0': 't',
                '1': 'u',
                '2': 'v',
            },
            '22': {
                '0': 'w',
                '1': 'x',
                '2': 'y',
                '3': 'z',
            },
            '300': 'Accept',
            '301': 'Delete last',
            '302': 'Delete all',
            '310': 'Back',
        }

    def display(self, screen, *args, **kwargs):
        screen.addstr(0, 0, KeypadWidget.caption)

        ys = [4, 12, 20]
        xs = [8, 26, 44]

        self._display_group(screen, (ys[0], xs[0]), '00', self._options['00'])
        self._display_group(screen, (ys[0], xs[2]), '01', self._options['01'])

        self._display_group(screen, (ys[1], xs[0]), '10', self._options['10'])
        self._display_group(screen, (ys[1], xs[1]), '11', self._options['11'])
        self._display_group(screen, (ys[1], xs[2]), '12', self._options['12'])

        self._display_group(screen, (ys[2], xs[0]), '20', self._options['20'])
        self._display_group(screen, (ys[2], xs[1]), '21', self._options['21'])
        self._display_group(screen, (ys[2], xs[2]), '22', self._options['22'])

        screen.addstr(ys[2] + 7, xs[0] - 6, 'Result: ' + self._internal_buffer)
        screen.addstr(ys[2] + 8, xs[0] - 6, '300: ' + self._options['300'])
        screen.addstr(ys[2] + 9, xs[0] - 6, '301: ' + self._options['301'])
        screen.addstr(ys[2] + 10, xs[0] - 6, '302: ' + self._options['302'])
        screen.addstr(ys[2] + 11, xs[0] - 6, '310: ' + self._options['310'])

    def _display_group(self, screen, pos, key, group):
        (y, x) = pos

        self._display_key(screen, y, x, key)

        if '0' in group:
            screen.addstr(y - 2, x - 1, '0: ' + group['0'])
        if '1' in group:
            screen.addstr(y, x + len(key) + 2, '1: ' + group['1'])
        if '2' in group:
            screen.addstr(y + 2, x - 1, '2: ' + group['2'])
        if '3' in group:
            screen.addstr(y, x - 6, '3: ' + group['3'])

    def _display_key(self, screen, y, x, key):
        screen.addstr(y, x, key)

        screen.addstr(y - 1, x, '--')
        screen.addstr(y, x + len(key), '|')
        screen.addstr(y + 1, x, '--')
        screen.addstr(y, x - 1, '|')

    def _display_hr(self, screen, y, x0, x1):
        screen.addstr(y, x0, '-' * (x1 - x0))

    def handle_input(self, u_in):
        self.current_option_code += u_in

        if len(self.current_option_code) > 3:
            raise GeneratorError('Not supported operation in KeypadWidget.')
        elif len(self.current_option_code) == 3:
            self._handle_submission_code(self.current_option_code)

    def _handle_submission_code(self, u_in):
        if u_in == '300':
            self._execution_observer.notify(self._internal_buffer)
        elif u_in == '301':
            self._internal_buffer = self._internal_buffer[:-1]
        elif u_in == '302':
            self._internal_buffer = ''
        elif u_in == '310':
            GeneratorStateMaster().pop_state()
        else:
            self._add_to_internal_buffer(u_in)

        self.current_option_code = ''

    def _add_to_internal_buffer(self, option_code):
        try:
            option_key = option_code[0:2]
            letter_key = option_code[-1:]
            option_letter = self._options[option_key][letter_key]

            self._internal_buffer += option_letter
        except KeyError:
            raise GeneratorError('Not supported operation in KeypadWidget.')
