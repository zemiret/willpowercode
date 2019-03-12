from generator import GeneratorStateMaster
from generator.widgets import GeneratorWidget


class CommonWidget(GeneratorWidget):
    caption = 'Common'

    def display(self, screen, *args, **kwargs):
        screen.addstr(0, 0, "You're in common generator")

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()

