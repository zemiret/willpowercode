from abc import ABC, abstractmethod


class GeneratorWidget(ABC):
    # TODO: Most generators will have the same "map to action" logic. Consider generalization
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