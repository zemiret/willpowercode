from generator import Generator, GeneratorMaster, FunctionGenerator, StatementGenerator, NumericKeypad


class TopLevelGenerator(Generator):
    @property
    def caption(self):
        return self._caption

    def __init__(self):
        self._caption = 'Top level'
        master = GeneratorMaster()
        
        self._options = {
            '0': {
                'caption': NumericKeypad.caption,
                'action': lambda: master.append_state(NumericKeypad())
            },
            '1': {
                'caption': FunctionGenerator.caption,
                'action': lambda: master.append_state(FunctionGenerator())
            },
            '2': {
                'caption': StatementGenerator.caption,
                'action': lambda: master.append_state(StatementGenerator())
            },
            '3': {
                'caption': FunctionGenerator.caption,
                'action': lambda: master.append_state(FunctionGenerator())
            },
        }

    def display(self, screen):
        screen.clear()
        for i, (key, val) in enumerate(self._options.items()):
            screen.addstr(i, 0, key + ': ' + self._options[key]['caption'])
        screen.refresh()

    def handle_input(self, u_in):
        int_in = int(u_in)
        if not 0 <= int_in <= 3:
            return

        self._options[str(u_in)]['action']()

    def reset(self):
        pass

