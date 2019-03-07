from generator import GeneratorStateMaster
from generator.widgets import GeneratorWidget


class CommonWidget(GeneratorWidget):
    caption = 'Common'

    def display(self, screen, *args, **kwargs):
        screen.clear()
        screen.addstr("You're in common generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()

