from generator.buffers import GeneratorBuffers
from generator.exceptions import GeneratorError
from generator.execution_observers import ExecutionObserver


class KeypadExecutionObserver(ExecutionObserver):
    def __init__(self):
        super().__init__()

        self._internal_buffer = ''

        self._accept_key = '300'
        self._delete_last_key = '301'

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
        }

    def notify(self, u_in: str):
        if u_in == self._accept_key:
            GeneratorBuffers().input.put(self._internal_buffer)
        elif u_in == self._delete_last_key:
            self._internal_buffer = self._internal_buffer[0:-1]
        else:
            self._handle_write(u_in)

    def _handle_write(self, u_in):
        if len(u_in) != 3:
            raise GeneratorError('Not supported operation in KeypadExecutionObserver.')

        try:
            option_key = u_in[0:2]
            letter_key = u_in[-1:]
            option_letter = self._options[option_key][letter_key]

            self._internal_buffer += option_letter
        except KeyError:
            raise GeneratorError('Not supported operation in KeypadExecutionObserver.')
