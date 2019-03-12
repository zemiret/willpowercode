import os
import subprocess

from utils.common import abs_path, tmp_file_path


class Commander(object):
    class __SingletonStub(object):
        def __init__(self):
            self._command_chain = []
            self._output_file = ''
            self._save_and_quit_command = abs_path(__file__, 'scripts', 'common', 'save_and_quit')

            self._commands_filepath = tmp_file_path()

        def append_command(self, command_path):
            self._command_chain.append(command_path)

        def pop_command(self):
            if len(self._command_chain) > 0:
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

    __instance = None

    def __init__(self):
        if Commander.__instance is None:
            Commander.__instance = Commander.__SingletonStub()

    def init(self, output_file):
        """
        Remember to call this method after first init!
        :param output_file: path to output file
        """
        Commander.__instance._output_file = output_file

    def __getattr__(self, item):
        return getattr(self.__instance, item)
