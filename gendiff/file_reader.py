"""Functions to read a file and return its content."""
import json
import os

import yaml


def read_file(file_path):
    """Read file and return its content as a dict.

    Args:
        file_path (str): path to the file

    Returns:
        dict: file content as dictionary
    """
    extension = os.path.basename(file_path).split('.')[-1]
    with open(file_path, 'r') as inp_f:
        if extension in {'yaml', 'yml'}:
            return yaml.safe_load(inp_f)
        return json.load(inp_f)
