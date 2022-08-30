"""Main module."""
import argparse

from gendiff import generate_diff

DESCRIPTION = 'Compares two configuration files and shows a difference.'


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
    print(generate_diff(args.first_file, args.second_file, args.format))


if __name__ == '__main__':
    main('tests/fixtures/1.json', 'tests/fixtures/2.json', format='json')
