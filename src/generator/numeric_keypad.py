from generator.base import GeneratorMaster, Generator


class NumericKeypad(Generator):
    caption = 'Numeric keypad'

    def __init__(self):
        pass

    def reset(self):
        pass

    def display(self, screen):
        screen.clear()
        screen.addstr("You're in function generator")
        screen.refresh()

    def handle_input(self, u_in):
        GeneratorMaster().reset_state()
