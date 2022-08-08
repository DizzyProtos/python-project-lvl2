"""This module does blah blah."""
import argparse
import json
# from gendiff.scripts.file_reader import read_file
from file_reader import read_file

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


def dict_to_lines(initial_key, input_dict, symb=''):
    lines = ['{0} {1}: {{'.format(symb, initial_key)]
    for key in input_dict:
        if isinstance(input_dict[key], dict):
            lines.append(dict_to_lines(key, input_dict[key], ''))
        else:
            lines.append(['{0}: {1}'.format(key, input_dict[key])])
    lines.append('}')
    return lines


def get_sub_add_line(key, value, symb='+'):
    if key == 'group3':
        print(1)
    
    if isinstance(value, dict):
        return dict_to_lines(key, value, symb)
    
    return ['{0} {1}: {2}'.format(symb, key, value)]


def find_difference_at_key(key, first_dict, second_dict):
    """Summary.

    Args:
        key (_type_): _description_
        first_value (_type_): _description_
        second_value (_type_): _description_

    Returns:
        _type_: _description_
    """
    first_value = first_dict.get(key, None)
    second_value = second_dict.get(key, None)
    if isinstance(first_value, dict) and isinstance(second_value, dict):
        return []
    if key not in first_dict:  # added
        return get_sub_add_line(key, second_value, '+')
    elif key not in second_dict:  # removed
        return get_sub_add_line(key, first_value, '-')
    elif first_value == second_value:  # equal
        return get_sub_add_line(key, first_value, '')
    elif first_value != second_value:  # changed
        lines = get_sub_add_line(key, first_value, '-')
        lines += get_sub_add_line(key, second_value, '+')
        return lines


def get_diff_lines(first_dict, second_dict):
    """Return difference between first and second dicts on key.
       nested lists are equal to nested dicts in the 1st file

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
        if isinstance(first_value, dict) and isinstance(second_value, dict):
            diff_lines.append('{0}: {{'.format(key))
            diff_lines.append(get_diff_lines(first_value, second_value))
            diff_lines.append('}')

        diff_lines += find_difference_at_key(key, first_dict, second_dict)
    return diff_lines


def format_diff_message(diff_lines, nest_level=1):
    diff_message = ''
    for line in diff_lines:
        if isinstance(line, list):
            diff_message += format_diff_message(line, nest_level+1)
        else:
            diff_message += '{0}{1}\n'.format('\t'*nest_level, line)
    if nest_level == 1:
        diff_message = '{{\n{0}}}'.format(diff_message)
    return diff_message


def generate_diff(file_path1, file_path2):
    """Summary.

    Args:
        file_path1 (_type_): _description_
        file_path2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    first_dict = read_file(file_path1)
    second_dict = read_file(file_path2)

    diff_lines = get_diff_lines(first_dict, second_dict)
    diff_message = format_diff_message(diff_lines)
    print(diff_message)

    return diff_message


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
