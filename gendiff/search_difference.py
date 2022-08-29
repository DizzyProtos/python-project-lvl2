"""Functions to get difference messages between two files."""


def get_alphabetical_keys(first_dict, second_dict):
    """Get keys from both dictionaries in alphabetical order.

    Args:
        first_dict (dict): first dictionary
        second_dict (dict): second dictionary

    Returns:
        list: unique keys from both dictionaries sorted alphabeticaly
    """
    return sorted(set(list(first_dict) + list(second_dict)))


def get_diff_at_key(key, first_dict, second_dict):
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
        line = ('a', key, second_value)
    elif key not in second_dict:  # removed
        line = ('s', key, first_value)
    elif first_value == second_value:  # equal
        line = ('e', key, first_value)
    elif first_value != second_value:  # changed
        line = ('u', key, (first_value, second_value))

    return (line)


def get_diff_lines(first_dict, second_dict):
    """Return difference between first and second dicts on key.

    Args:
        first_dict (dict): original dictionary
        second_dict (dict): changed dictionary

    Returns:
        list: lines with differences
    """
    diff_lines = []
    for key in get_alphabetical_keys(first_dict, second_dict):
        first_value = first_dict.get(key, None)
        second_value = second_dict.get(key, None)
        if key == 'group4':
            print(1)
        if isinstance(first_value, dict) and isinstance(second_value, dict):
            diff_lines.append(key)
            diff_lines.append(get_diff_lines(first_value, second_value))
        else:
            diff_lines.append(get_diff_at_key(key, first_dict, second_dict))
    return diff_lines
