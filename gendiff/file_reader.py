"""Functions to read a file and return its content."""
import os
import json

import yaml


def _get_file_format(file_path):
    """Get file format from path.

    Args:
        file_path (str): path to the file

    Returns:
        str: file format
    """
    return os.path.basename(file_path).split('.')[-1]


def _parse_json(file_handler):
    """Parses JSON file and return dictionary.

    Args:
        file_handler (file): file to parse

    Returns:
        dict: dictionary from the file
    """
    return json.load(file_handler)


def _parse_yaml(file_handler):
    """Parses YAML file and returns dictionary.

    Args:
        file_handler (file): file to parse

    Returns:
        dict: dictionary from the file
    """
    return yaml.safe_load(file_handler)


_FILE_READERS = {'yaml': _parse_yaml, 'yml': _parse_yaml,
                 'json': _parse_json, 'default': _parse_json}


def read_file(file_path):
    """Read file and return its content as a dict.

    Args:
        file_path (str): path to the file

    Returns:
        dict: file content as dictionary
    """
    format = _get_file_format(file_path)
    if format not in _FILE_READERS:
        format = 'default'
    with open(file_path, 'r') as inp_f:
        return _FILE_READERS[format](inp_f)
