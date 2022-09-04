"""Get difference message for two files."""

from gendiff.file_reader import read_file
from gendiff.formaters.format_difference import format_message, is_format_valid
from gendiff.search_difference import get_diff


def generate_diff(file_path1, file_path2, format_name='stylish'):
    """Get difference between two files.

    Args:
        file_path1 (str): path to the first file
        file_path2 (str): path to the second file
        format_name (str): format of the output message

    Returns:
        str: description of changes in the first file
    """
    if not format_name:
        format_name = 'stylish'
    if not is_format_valid(format_name):
        return f'Format name {format_name} is not found'

    first_dict = read_file(file_path1)
    second_dict = read_file(file_path2)

    diff_lines = get_diff(first_dict, second_dict)
    return format_message(diff_lines, format_name)
