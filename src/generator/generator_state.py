from generator.buffers import GeneratorBuffers


class GeneratorStateMaster(object):
    class __SingletonStub(object):
        def __init__(self):
            self._start_state = None
            self._current_state = None
            self._state_chain = []

            self._screen = None
            self._buffers = None

        def set_start_state(self, start_state):
            self._start_state = start_state

        def reset_state(self):
            self._start_state = self._start_state.__class__()  # Recreate start state
            self._state_chain = []
            self.append_state(self._start_state)

        def display(self):
            self._screen.clear()
            self._buffers.display(self._screen)
            self._current_state.display(self._screen)
            self._screen.refresh()

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

    def __init__(self):
        if GeneratorStateMaster.__instance is None:
            GeneratorStateMaster.__instance = GeneratorStateMaster.__SingletonStub()

    def init(self, screen, buffers: GeneratorBuffers):
        GeneratorStateMaster.__instance._screen = screen
        GeneratorStateMaster.__instance._buffers = buffers

    def __getattr__(self, item):
        return getattr(self.__instance, item)
