from typing import Tuple

from generator.exceptions import GeneratorBufferError
from generator.buffers.buffer import Buffer
from generator.widget_base import Widget


class NavigationBuffer(Buffer):
    def __init__(self):
        super().__init__()
        self._navigation_state = (0, 0)  # line, pos in line

    def make_command(self):
        pass

    def put(self, nav_state: Tuple[int, int]):
        """
        :param nav_state: First position is line in file, second is position in line
        """
        if nav_state[0] >= 0 and nav_state[1] >= 0:
            self._navigation_state = nav_state
        else:
            raise GeneratorBufferError('Cannot set navigation to negative lines in NavigationBuffer.')

    def peek(self):
        return self._navigation_state

    def clear(self):
        self._navigation_state = (0, 0)


class NavigationBufferWidget(Widget):
    def __init__(self, nav_buffer: Buffer):
        self._buffer = nav_buffer

    def display(self, screen, *args, **kwargs):
        """
        :param args: should be (y, x) with position to display on the screen
        :param kwargs: optional reverse argument. If set, the x position is assumed to be the end position
        :return None
        """
        text = "{}L:{}c".format(self._buffer.peek()[0], self._buffer.peek()[1])
        y, x = args[0]

        if 'reverse' in kwargs and kwargs['reverse'] is True:
            x = self.cols(screen) - len(text) - 1

        screen.addstr(y, x, text)
