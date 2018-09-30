from abc import ABC, abstractmethod


class Generator(ABC):
    @abstractmethod
    def display(self, screen):
        pass

    @abstractmethod
    def handle_input(self, u_in):
        pass

    @abstractmethod
    def reset(self):
        """
        Should restore the generator object to the state in which it can be added to the genrators tree
        """
        pass


class GeneratorMaster(object):
    class __SingletonStub(object):
        def __init__(self):
            self._start_state = None
            self._current_state = None
            self._state_chain = []

        def set_start_state(self, start_state):
            self._start_state = start_state

        def reset_state(self):
            self._start_state.reset()
            self._state_chain = []
            self.append_state(self._start_state)

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


