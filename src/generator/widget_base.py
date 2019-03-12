from abc import ABC, abstractmethod


class Widget(ABC):
    def cols(self, screen):
        return screen.getmaxyx()[1]

    def rows(self, screen):
        return screen.getmaxyx()[0]

    @abstractmethod
    def display(self, screen, *args, **kwargs):
        pass
