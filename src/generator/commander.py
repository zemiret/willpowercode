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
            self._history_filepath = abs_path(__file__, '..', '..', 'out', 'history')

        def append_command(self, command_path):
            self._command_chain.append(command_path)

        def pop_command(self):
            if len(self._command_chain) > 0:
                self._command_chain.pop()

        def execute(self):
            with open(self._commands_filepath, 'w+') as command_file, \
                 open(self._history_filepath, 'a+') as history_file:

                for command in self._command_chain:
                    self._write_command(command_file, history_file, command)

                self._write_command(command_file, history_file, self._save_and_quit_command)

                command_file.close()
                history_file.close()

                subprocess.run(['vim', '-s', os.path.realpath(command_file.name), self._output_file], shell=False)

                self.clear_commands()

        def _write_command(self, output_file, history_file, command_file):
            with open(command_file, 'r') as command_content_file:
                command_content = command_content_file.read()

                output_file.write(command_content)
                history_file.write(command_content)

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
