from abc import ABC, abstractmethod


class ExecutionObserver(ABC):
    @abstractmethod
    def notify(self, u_in: str):
        pass


# TODO: Stub observers for testing and observation
class PrintObserver(ExecutionObserver):
    def notify(self, u_in: str):
        print(u_in)


class ReturnObserver(ExecutionObserver):
    def notify(self, u_in: str):
        return u_in
