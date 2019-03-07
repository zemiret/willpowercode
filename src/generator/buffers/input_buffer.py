from generator.buffers.buffer import Buffer
from generator.widgets import Widget


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
    def display(self, screen, *args, **kwargs):
        pass
