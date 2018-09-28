class TestGenerator(object):
    def __init__(self):
        self._options = {
            '2': {
                'caption': 'Meow meow!',
                'action': lambda screen: screen.addstr(0, 0, 'Meow meow')

            },
            '3': {
                'caption': 'Power rangers!',
                'action': lambda screen: screen.addstr(0, 0, 'Power')
            },
            '4': {
                'caption': 'Woof woof!',
                'action': lambda screen: screen.addstr(0, 0, 'Trogdor!')
            },
            '5': {
                'caption': 'Horse sounds',
                'action': lambda screen: screen.addstr(0, 0, 'IIIIHA')
            }
        }

    def display(self, screen):
        screen.clear()
        for i, option in enumerate(self._options):
            screen.addstr(i, 0, option[i + 2]['caption'])
        screen.refresh()

    def handle_input(self, screen, u_in):
        screen.clear()
        self._options[u_in]['action']()
        screen.refresh()
