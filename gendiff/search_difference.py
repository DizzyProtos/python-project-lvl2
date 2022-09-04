"""Functions to get difference messages between two files."""
from gendiff.difference_description import ADD, REMOVE, UPDATE, SAME, NESTED


def _get_alphabetical_keys(first_dict, second_dict):
    """Get keys from both dictionaries in alphabetical order.

    Args:
        first_dict (dict): first dictionary
        second_dict (dict): second dictionary

    Returns:
        list: unique keys from both dictionaries sorted alphabeticaly
    """
    return sorted(set(list(first_dict) + list(second_dict)))


def _get_diff_at_key(key, first_dict, second_dict):
    """Get difference line at a key.

    Args:
        key (str): key to find a difference at
        first_dict (dict): first original dict
        second_dict (dict): second changed dict

    Returns:
        tuple: difference line
    """
    first_value = first_dict.get(key, None)
    second_value = second_dict.get(key, None)
    if isinstance(first_value, dict) and isinstance(second_value, dict):
        line = ()
    if key not in first_dict:  # added
        line = (ADD, key, second_value)
    elif key not in second_dict:  # removed
        line = (REMOVE, key, first_value)
    elif first_value == second_value:  # equal
        line = (SAME, key, first_value)
    elif first_value != second_value:  # changed
        line = (UPDATE, key, (first_value, second_value))

    return (line)


def get_diff(first_dict, second_dict):
    """Return difference between first and second dicts on key.

    Args:
        first_dict (dict): original dictionary
        second_dict (dict): changed dictionary

    Returns:
        list: lines with differences
    """
    diff_lines = []
    for key in _get_alphabetical_keys(first_dict, second_dict):
        first_value = first_dict.get(key, None)
        second_value = second_dict.get(key, None)
        if isinstance(first_value, dict) and isinstance(second_value, dict):
            nested_diff = get_diff(first_value, second_value)
            diff_lines.append((NESTED, key, nested_diff))
        else:
            diff_lines.append(_get_diff_at_key(key, first_dict, second_dict))
    return diff_lines
