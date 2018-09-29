class TestGenerator(object):
    def __init__(self):
        self._options = {
            '0': {
                'caption': 'Meow meow!',
                'action': 'Meow meow'
            },
            '1': {
                'caption': 'Power rangers!',
                'action': 'Power'
            },
            '2': {
                'caption': 'Woof woof!',
                'action': 'Trogdor!'
            },
            '3': {
                'caption': 'Horse sounds',
                'action': 'IIIIHA'
            }
        }

        self.current = None

    def display(self, screen):
        screen.clear()
        for i, (key, val) in enumerate(self._options.items()):
            screen.addstr(i, 0, key + ': ' + val['caption'])

        if self.current is not None:
            screen.addstr(len(self._options.items()) + 1, 0, self.current)
        screen.refresh()

    def handle_input(self, u_in):
        self.current = self._options[str(u_in)]['action']
