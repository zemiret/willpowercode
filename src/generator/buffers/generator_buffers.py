from generator.buffers.input_buffer import InputBuffer
from generator.buffers.navigation_buffer import NavigationBuffer
from generator.widgets import Widget


class GeneratorBuffers(Widget):
    def __init__(self):
        self._nav_buffer = NavigationBuffer()
        self._input_buffer = InputBuffer()

    def display(self, screen, *args, **kwargs):
        pass
