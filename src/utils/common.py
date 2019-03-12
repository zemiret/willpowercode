import os
import tempfile
import uuid


def abs_path(file, *args):
    """
    :param file: __file__ path to which the path is relatively resolved
    :param args: the rest of the path, just like args to os.path.join
    :return: resolved path
    """
    return os.path.join(os.path.dirname(os.path.realpath(file)), *args)


def tmp_file_path():
    return os.path.join(tempfile.gettempdir(), uuid.uuid1().hex)
