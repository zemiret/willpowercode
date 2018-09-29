import generator.base as base


class StatementGenerator(base.Generator):
    caption = 'Statements'

    def display(self, screen):
        screen.clear()
        screen.add_str("You're in statement generator")
        screen.refresh()

    def handle_input(self, u_in):
        base.GeneratorMaster().reset_state()
