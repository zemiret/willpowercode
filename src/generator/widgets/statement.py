from generator import GeneratorStateMaster
from . import GeneratorWidget


class StatementWidget(GeneratorWidget):
    caption = 'Statements'

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in statement generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
