from generator import GeneratorStateMaster
from generator.widgets import GeneratorWidget


class RefactorWidget(GeneratorWidget):
    caption = 'Refactor'

    def display(self, screen, *args, **kwargs):
        screen.addstr(0, 0, "You're in refactor generator")

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
