"""Main module."""
import argparse

from gendiff.scripts.file_reader import read_file
from gendiff.scripts.format_difference import format_diff_message
from gendiff.scripts.search_difference import get_diff_lines

DESCRIPTION = 'Compares two configuration files and shows a difference.'


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


def main(*args, **kwargs):
    """Get difference between two files.

    Args:
        *args (list): arguments
        **kwargs (dict): named arguments

    Returns:
        str: description of files differences
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)

    help_format = 'set format of output'
    parser.add_argument('-f', '--format', dest='format', help=help_format)

    args = parser.parse_args()

    return generate_diff(args.first_file, args.second_file, 'plain')


if __name__ == '__main__':
    main('tests/fixtures/1.json', 'tests/fixtures/2.json')
