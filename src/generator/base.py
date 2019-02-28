import os
import subprocess

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

        self._commands_filepath = os.path.realpath(os.path.join(os.environ['HOME'], 'tmp', 'commands'))

    def append_command(self, command_path):
        self._command_chain.append(command_path)

    def pop_command(self):
        self._command_chain.pop()

    def execute(self):
        with open(self._commands_filepath, 'w+') as command_file:
            for command in self._command_chain:
                with open(command, 'r') as command_content:
                    command_file.write(command_content.read())

            with open(self._save_and_quit_command, 'r') as quit_cmd:
                command_file.write(quit_cmd.read())

            print(command_file.name)

            command_file.close()

            subprocess.run(['vim', '-s', os.path.realpath(command_file.name), self._output_file], shell=False)

            self.clear_commands()

    def clear_commands(self):
        self._command_chain = []


class GeneratorMaster(object):
    class __SingletonStub(object):
        def __init__(self, output_file, screen):
            self.commander = Commander(output_file)

            self._start_state = None
            self._current_state = None
            self._state_chain = []

            self._screen = screen

        def set_start_state(self, start_state):
            self._start_state = start_state

        def reset_state(self):
            self._start_state.reset()
            self._state_chain = []
            self.append_state(self._start_state)

        def display(self):
            self._current_state.display(self._screen)

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

    __instance = None

    def __init__(self, screen=None, output_file=None):
        if GeneratorMaster.__instance is None:
            if output_file is None:
                raise AttributeError('GeneratorMaster requires output_file!')
            if screen is None:
                raise AttributeError('GeneratorMaster requires screen!')

            GeneratorMaster.__instance = GeneratorMaster.__SingletonStub(output_file, screen)

    def __getattr__(self, item):
        return getattr(self.__instance, item)


