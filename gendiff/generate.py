"""Main module."""

from gendiff.file_reader import read_file
from gendiff.format_difference import format_diff_message
from gendiff.search_difference import get_diff_lines


def generate_diff(file_path1, file_path2, format_name='json'):
    """Get difference between two files.

    Args:
        file_path1 (str): path to the first file
        file_path2 (str): path to the second file
        format_name (str): format of the output message

    Returns:
        str: description of changes in the first file
    """
    first_dict = read_file(file_path1)
    second_dict = read_file(file_path2)

    diff_lines = get_diff_lines(first_dict, second_dict)
    return format_diff_message(diff_lines, format_name)
