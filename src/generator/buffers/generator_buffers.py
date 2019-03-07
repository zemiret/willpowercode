from generator.buffers.input_buffer import InputBuffer, InputBufferWidget
from generator.buffers.navigation_buffer import NavigationBuffer, NavigationBufferWidget
from generator.widget_base import Widget


class GeneratorBuffers(Widget):
    def __init__(self):
        self._nav_buffer_widget = NavigationBufferWidget(NavigationBuffer())
        self._input_buffer_widget = InputBufferWidget(InputBuffer())

    def display(self, screen, *args, **kwargs):
        pass
