from generator import GeneratorStateMaster
from . import GeneratorWidget


class NavigationGeneratorWidget(GeneratorWidget):
    caption = 'Navigation'

    def reset(self):
        pass

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in navigation generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
