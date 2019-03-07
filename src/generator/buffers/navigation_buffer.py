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
    def __init__(self, nav_buffer):
        self._buffer = nav_buffer

    def display(self, screen, *args, **kwargs):
        """
        :param args: should be a tuple with (y, x) position on the screen
        :return: None
        """
        pass
