import os
import subprocess

import tempfile
from abc import ABC, abstractmethod

from utils.common import abs_path


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


class Commander(object):
    def __init__(self, output_file):
        self._command_chain = []
        self._output_file = output_file
        self._save_and_quit_command = abs_path(__file__, 'scripts', 'common', 'save_and_quit')

    def append_command(self, command_path):
        self._command_chain.append(command_path)

    def pop_command(self):
        self._command_chain.pop()

    def execute(self):
        with tempfile.NamedTemporaryFile('a+') as command_file:
            for command in self._command_chain:
                with open(command, 'r') as command_content:
                    command_file.write(command_content.read())

            with open(self._save_and_quit_command, 'r') as quit_cmd:
                command_file.write(quit_cmd.read())

            subprocess.run(['vim', '-s', os.path.realpath(command_file.name), self._output_file], shell=False)
            command_file.close()

            self.clear_commands()

    def clear_commands(self):
        self._command_chain = []


class GeneratorMaster(object):
    class __SingletonStub(object):
        def __init__(self, output_file):
            self.commander = Commander(output_file)

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

    def __init__(self, output_file=None):
        if GeneratorMaster.__instance is None:
            if output_file is None:
                raise AttributeError('The initialization of GeneratorMaster requires output_file supplied!')

            GeneratorMaster.__instance = GeneratorMaster.__SingletonStub(output_file)

    def __getattr__(self, item):
        return getattr(self.__instance, item)


