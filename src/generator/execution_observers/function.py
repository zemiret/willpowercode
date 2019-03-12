from generator import Commander, GeneratorStateMaster
from generator.buffers import GeneratorBuffers
from generator.exceptions import GeneratorError
from generator.execution_observers import ExecutionObserver
from utils.common import abs_path
from generator.scripts import create_script


class FunctionExecutionObserver(ExecutionObserver):
    def __init__(self):
        super().__init__()

        def _decorator_action():
            command = _create_command(abs_path(__file__, '..', 'scripts', 'function', 'decorator'))

            Commander().append_command(command)
            Commander().execute()

        def _definition_action():
            command = _create_command(abs_path(__file__, '..', 'scripts', 'function', 'definition'))

            Commander().append_command(command)
            Commander().execute()

        def _create_command(script_path):
            decorator_name = GeneratorBuffers().input.peek()
            return create_script(script_path, decorator_name)

        self._options = {
            '0': _decorator_action,
            '1': _definition_action,
            '2': lambda: GeneratorStateMaster().pop_state()
        }

    def notify(self, u_in: str):
        try:
            self._options[str(u_in)]()
        except KeyError:
            raise GeneratorError('Not supported operation in FunctionExecutionObserver.')
