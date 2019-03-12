from utils.common import tmp_file_path


def create_script(path, *args, **kwargs):
    """
    Uses path as a blueprint to interpolate the script using python3 string 'format' method.
    Returns the path to the newly created script.

    :param path: string path to original script
    :return: str: string path to generated script
    """
    script_file = open(path, 'r')

    content = script_file.read()
    content = content.format(*args, **kwargs)

    out_file_path = tmp_file_path()
    out_file = open(out_file_path, 'w+')
    out_file.write(content)

    return out_file_path
