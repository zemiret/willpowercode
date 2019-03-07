from typing import Tuple

from generator.buffers.buffer import Buffer
from generator.exceptions import GeneratorBufferException
from generator.widgets import Widget


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
            raise GeneratorBufferException('Cannot set navigation to negative lines in NavigationBuffer.')

    def peek(self):
        return self._navigation_state

    def clear(self):
        self._navigation_state = (0, 0)


class NavigationBufferWidget(Widget):
    def display(self, screen, *args, **kwargs):
        """
        :param args: should be a tuple with (y, x) position on the screen
        :return: None
        """
        pass
