from generator.base import Generator, GeneratorMaster


class StatementGenerator(Generator):
    caption = 'Statements'

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in statement generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorMaster().reset_state()

    def reset(self):
        pass
