"""This module does blah blah."""
import argparse
import json

DESCRIPTION = 'Compares two configuration files and shows a difference.'


def get_alphabetical_keys(first_dict, second_dict):
    """Get keys from both dictionaries in alphabetical order.

    Args:
        first_dict (dict): first dictionary
        second_dict (dict): second dictionary

    Returns:
        list: unique keys from both dictionaries sorted alphabeticaly
    """
    return sorted(set(list(first_dict) + list(second_dict)))


def get_diff_lines(key, first_value, second_value):
    """Summary.

    Args:
        key (_type_): _description_
        first_value (_type_): _description_
        second_value (_type_): _description_

    Returns:
        _type_: _description_
    """
    if first_value is None:  # added
        return ['+{0}: {1}'.format(key, second_value)]
    elif second_value is None:  # removed
        return ['-{0}: {1}'.format(key, first_value)]
    elif first_value == second_value:  # equal
        return ['{0}: {1}'.format(key, first_value)]
    elif first_value != second_value:  # changed
        lines = ['-{0}: {1}'.format(key, first_value)]
        lines.append('+{0}: {1}'.format(key, second_value))
        return lines


def get_diff_message(first_dict, second_dict):
    """Return difference between first and second dicts on key.

    Args:
        first_dict (dict): original dictionary
        second_dict (dict): changed dictionary

    Returns:
        str: _description_
    """
    diff_lines = []
    for key in get_alphabetical_keys(first_dict, second_dict):
        first_value = first_dict.get(key, None)
        second_value = second_dict.get(key, None)
        diff_lines += get_diff_lines(key, first_value, second_value)
    diff_message = '\n'.join(['\t{0}'.format(line) for line in diff_lines])
    diff_message = '{{ \n {0} \n}}'.format(diff_message)
    return diff_message


def generate_diff(file_path1, file_path2):
    """Summary.

    Args:
        file_path1 (_type_): _description_
        file_path2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path1, 'r') as f1:
        first_dict = json.load(f1)
    with open(file_path2, 'r') as f2:
        second_dict = json.load(f2)

    return get_diff_message(first_dict, second_dict)


def main(*args, **kwargs):
    """Summary.

    Args:
        *args (list): arguments
        **kwargs (dict): named arguments

    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)

    help_format = 'set format of output'
    parser.add_argument('-f', '--format', dest='format', help=help_format)

    args = parser.parse_args()

    return generate_diff(args.first_file, args.second_file)


if __name__ == '__main__':
    main()
