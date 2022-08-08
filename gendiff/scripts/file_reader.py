import os
import json
import yaml


def read_file(file_path):
    """Summary.

    Args:
        file_path (str): path to the json or yaml file

    Returns:
        dict: file content as dictionary
    """
    extension = os.path.basename(file_path).split('.')[-1]
    with open(file_path, 'r') as f:
        if extension == 'yaml' or extension == 'yml':
            return yaml.load(f, Loader=yaml.CLoader)
        return json.load(f)
