from generator.buffers.buffer import Buffer
from generator.widget_base import Widget


class InputBuffer(Buffer):
    def __init__(self):
        super().__init__()
        self._buffer = ""

    def make_command(self):
        pass

    def put(self, val):
        self._buffer += str(val)

    def peek(self):
        return self._buffer

    def clear(self):
        self._buffer = ""


class InputBufferWidget(Widget):
    def __init__(self, input_buffer: Buffer):
        self._buffer = input_buffer

    def display(self, screen, *args, **kwargs):
        """
        :param args: should be (y, x) with position to display on the screen
        :param kwargs: optional reverse argument. If set, the x position is assumed to be the end position
        :return None
        """
        text = 'Text buffer: {}'.format(self._buffer.peek())
        y, x = args[0]
        if 'reverse' in kwargs and kwargs['reverse'] is True:
            x = self.cols(screen) - len(text) - 1

        screen.addstr(y, x, text)
