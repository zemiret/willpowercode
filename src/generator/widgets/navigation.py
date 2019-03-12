from generator import GeneratorStateMaster
from . import GeneratorWidget


class NavigationWidget(GeneratorWidget):
    caption = 'Navigation'

    def display(self, screen, *args, **kwargs):
        screen.addstr(0, 0, "You're in navigation generator")

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
