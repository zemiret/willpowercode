from generator import Generator, GeneratorMaster
from utils.common import abs_path


class NumericKeypad(Generator):
    caption = 'Numeric keypad'

    def __init__(self):
        master = GeneratorMaster()
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
            '2': {
                'caption': 'accept',
                'action': lambda: master.commander.execute()
            },
            '3': {
                'caption': 'back',
                'action': lambda: master.pop_state()
            }
        }

        self._input_options = {
            '00': {
                'caption': '0',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script0'))
            },
            '01': {
                'caption': '1',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script1'))
            },
            '02': {
                'caption': '2',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script2'))
            },
            '03': {
                'caption': '3',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script3'))
            },
            '10': {
                'caption': '4',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script4'))
            },
            '11': {
                'caption': '5',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script5'))
            },
            '12': {
                'caption': '6',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script6'))
            },
            '13': {
                'caption': '7',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script7'))
            },
            '20': {
                'caption': '8',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script8'))
            },
            '21': {
                'caption': '9',
                'action':
                    lambda: master.commander.append_command(abs_path(__file__, 'scripts', 'numeric_keypad', 'script9'))
            },
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
                self._input_options[self._cur_input + u_in]['action']()
                self._cur_input = ''
                self._input_mode = False
            else:
                self._cur_input = u_in
        else:
            self._options[u_in]['action']()
