from generator import GeneratorStateMaster
from . import GeneratorWidget


class NavigationWidget(GeneratorWidget):
    caption = 'Navigation'

    def display(self, screen, *args, **kwargs):
        screen.clear()
        screen.addstr("You're in navigation generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
