import os
import subprocess

import tempfile
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


class Commander(object):
    def __init__(self, output_file):
        self._command_chain = []
        self._output_file = output_file
        self._save_and_quit_command = \
            os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scripts', 'common', 'save_and_quit')

    def append_command(self, command_path):
        self._command_chain.append(command_path)

    def pop_command(self):
        self._command_chain.pop()

    def execute(self):
        command_file = tempfile.NamedTemporaryFile('a+b')
        for command in self._command_chain:
            with open(command, 'r') as command_content:
                command_file.write(command_content.read())

        with open(self._save_and_quit_command, 'r') as quit_cmd:
            command_file.write(quit_cmd.read())

        subprocess.run(['vim', '-s', command_file, self._output_file])
        command_file.close()

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

    def __init__(self):
        if GeneratorMaster.__instance is None:
            GeneratorMaster.__instance = GeneratorMaster.__SingletonStub()

    def __getattr__(self, item):
        return getattr(self.__instance, item)


