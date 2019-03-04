from generator import GeneratorWidget, GeneratorStateMaster


class StatementGeneratorWidget(GeneratorWidget):
    caption = 'Statements'

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in statement generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()

    def reset(self):
        pass
