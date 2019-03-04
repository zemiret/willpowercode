from generator import GeneratorStateMaster, GeneratorWidget


class FunctionGeneratorWidget(GeneratorWidget):
    caption = 'Functions'

    def reset(self):
        pass

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in function generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorStateMaster().reset_state()
