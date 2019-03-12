from generator.buffers import GeneratorBuffers
from generator.execution_observers import ExecutionObserver


class KeypadExecutionObserver(ExecutionObserver):
    def notify(self, u_in: str):
        GeneratorBuffers().input.put(u_in)
