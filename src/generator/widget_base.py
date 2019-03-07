from abc import ABC, abstractmethod


class Widget(ABC):
    @abstractmethod
    def display(self, screen, *args, **kwargs):
        pass
