from generator import GeneratorStateMaster
from . import GeneratorWidget


class StatementWidget(GeneratorWidget):
    caption = 'Statements'

    def display(self, screen, *args, **kwargs):
        screen.addstr(0, 0, "You're in statement generator")

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
