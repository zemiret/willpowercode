from generator import GeneratorStateMaster
from generator.widgets import GeneratorWidget


class RefactorWidget(GeneratorWidget):
    caption = 'Refactor'

    def display(self, screen, *args, **kwargs):
        screen.clear()
        screen.addstr("You're in refactor generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
