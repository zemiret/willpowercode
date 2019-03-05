class GeneratorStateMaster(object):
    class __SingletonStub(object):
        def __init__(self, screen):
            self._start_state = None
            self._current_state = None
            self._state_chain = []

            self._screen = screen

        def set_start_state(self, start_state):
            self._start_state = start_state

        def reset_state(self):
            self._start_state.reset()
            self._state_chain = []
            self.append_state(self._start_state)

        def display(self):
            self._current_state.display(self._screen)

        def handle_input(self, u_in):
            self._current_state.handle_input(u_in)

        def pop_state(self):
            if len(self._state_chain) > 1:
                self._state_chain.pop()
                self._current_state = self._state_chain[-1]
                self.display()

        def append_state(self, state):
            self._state_chain.append(state)
            self._current_state = state
            self.display()

    __instance = None

    def __init__(self, screen=None):
        if GeneratorStateMaster.__instance is None:
            if screen is None:
                raise TypeError('GeneratorStaterMaster initialization requires screen!')

            GeneratorStateMaster.__instance = GeneratorStateMaster.__SingletonStub(screen)

    def __getattr__(self, item):
        return getattr(self.__instance, item)
