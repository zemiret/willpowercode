from generator import Generator, GeneratorMaster


class NavigationGenerator(Generator):
    caption = 'Navigation'

    def reset(self):
        pass

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in navigation generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorMaster().reset_state()
