import generator.base as base


class FunctionGenerator(base.Generator):
    caption = 'Funcitons'

    def display(self, screen):
        screen.clear()
        screen.add_str("You're in funciton generator")
        screen.refresh()

    def handle_input(self, u_in):
        base.GeneratorMaster().reset_state()
