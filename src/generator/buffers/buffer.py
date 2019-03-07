import abc


class Buffer(abc.ABC):
    @abc.abstractmethod
    def make_command(self):
        """
        Create a command file from the buffer
        :return: Path to the file
        """
        pass

    @abc.abstractmethod
    def put(self, *args):
        """
        Put some argument into the buffer
        :return: None
        """
        pass

    @abc.abstractmethod
    def peek(self):
        """
        Get a preview of the value currently in buffer
        :return: value currently held in buffer
        """
        pass

    @abc.abstractmethod
    def clear(self):
        """
        Clear the buffer
        :return: None
        """
        pass