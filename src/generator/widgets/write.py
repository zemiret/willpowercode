from generator.base import make_generator_entry, make_pop_entry
from generator.exceptions import GeneratorError
from generator.execution_observers import ExecutionObserver
from generator.widgets import GeneratorWidget, WidgetsFactory
from generator.widgets.class_gen import ClassWidget
from generator.widgets.function import FunctionWidget
from generator.widgets.statement import StatementWidget


class WriteWidget(GeneratorWidget):
    caption = 'Write'

    def __init__(self, execution_observer: ExecutionObserver):
        super().__init__(execution_observer)

        self._options = {
            '0': make_generator_entry(FunctionWidget.caption, WidgetsFactory.make_function()),
            '1': make_generator_entry(ClassWidget.caption, WidgetsFactory.make_class()),
            '2': make_generator_entry(StatementWidget.caption, WidgetsFactory.make_statement()),
            '3': make_pop_entry(),
        }

    def display(self, screen, *args, **kwargs):
        super().display(screen)
        screen.addstr(0, 0, WriteWidget.caption)
        screen.refresh()

    def handle_input(self, u_in):
        try:
            print("Write action: {}".format(u_in))
            self._options[u_in]['action']()
        except KeyError:
            raise GeneratorError('Not handled action in WriteWidget')
