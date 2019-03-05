from generator import GeneratorStateMaster
from . import GeneratorWidget


class FunctionWidget(GeneratorWidget):
    caption = 'Functions'

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in function generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
