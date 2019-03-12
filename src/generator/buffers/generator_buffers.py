from generator.buffers.input_buffer import InputBuffer, InputBufferWidget
from generator.buffers.navigation_buffer import NavigationBuffer, NavigationBufferWidget
from generator.widget_base import Widget


class GeneratorBuffers(object):
    class __SingletonStub(Widget):
        def __init__(self):
            self._nav_buffer = NavigationBuffer()
            self._input_buffer = InputBuffer()

            self._nav_buffer_widget = NavigationBufferWidget(self._nav_buffer)
            self._input_buffer_widget = InputBufferWidget(self._input_buffer)

        def display(self, screen, *args, **kwargs):
            self._input_buffer_widget.display(
                screen,
                (self.rows(screen) - 1, 0),
                *args, **kwargs)
            self._nav_buffer_widget.display(
                screen,
                (self.rows(screen) - 1, self.cols(screen) - 1),
                reverse=True,
                *args, **kwargs)

        @property
        def nav(self):
            return self._nav_buffer

        @property
        def input(self):
            return self._input_buffer

    __instance = None

    def __init__(self):
        if GeneratorBuffers.__instance is None:
            GeneratorBuffers.__instance = GeneratorBuffers.__SingletonStub()

    def __getattr__(self, item):
        return getattr(self.__instance, item)
