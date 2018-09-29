from abc import ABC, abstractmethod

class Generator(ABC):
    @abstractmethod
    def display(self, screen):
        pass

    @abstractmethod
    def handle_input(self, u_in):
        pass


class GeneratorMaster(object):
    class __SingletonStub(object):
        def __init__(self):
            self._current_state = None
            self._state_chain = []
            self.reset_state()

        def reset_state(self):
            self._state_chain = []
            self.append_state(TopLevelGenerator())

        def display(self, screen):
            self._current_state.display(screen)

        def handle_input(self, u_in):
            self._current_state.handle_input(u_in)

        def pop_state(self):
            self._state_chain.pop()

        def append_state(self, state):
            self._state_chain.append(state)
            self._current_state = state

    __instance = None

    def __init__(self):
        if GeneratorMaster.__instance is None:
            GeneratorMaster.__instance = GeneratorMaster.__SingletonStub()

    def __getattr__(self, item):
        return getattr(self.__instance, item)


class TopLevelGenerator(Generator):
    @property
    def caption(self):
        return self._caption

    def __init__(self):
        self._caption = 'Top level'

        import generator.statement as statement
        import generator.function as fun

        master = GeneratorMaster()
        self._options = {
            '0': {
                'caption': statement.StatementGenerator.caption,
                'action': lambda: master.append_state(statement.StatementGenerator())
            },
            '1': {
                'caption': fun.FunctionGenerator.caption,
                'action': lambda: master.append_state(fun.FunctionGenerator())
            },
            '2': {
                'caption': statement.StatementGenerator.caption,
                'action': lambda: master.append_state(statement.StatementGenerator())
            },
            '3': {
                'caption': fun.FunctionGenerator.caption,
                'action': lambda: master.append_state(fun.FunctionGenerator())
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


