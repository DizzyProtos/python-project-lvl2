"""Create json difference message."""

import json


def _format_diff_json_child(type, key, line_val):
    """Construct single difference dict.

    Args:
        type (str): type of change
        key (str): changed key
        line_val (any): value of the difference lne

    Returns:
        dict: difference as a dictionary
    """
    if type == 'changed':
        value_dict = {'value1': line_val[0], 'value2': line_val[1]}
    else:
        value_dict = {'value': line_val}
    return {'key': key, 'type': type, **value_dict}


def _get_json_child(line_tuple):
    """Get difference dict for a single line.

    Args:
        line_tuple (tuple): difference line (symbol, key, value)

    Returns:
        dict: difference as a dictionary
    """
    symb, key, line_value = line_tuple
    type_verb = ''
    if symb == 'u':
        type_verb = 'changed'
    if symb == 'e':
        type_verb = 'unchanged'
    if symb == 'a':
        type_verb = 'added'
    if symb == 's':
        type_verb = 'deleted'
    return _format_diff_json_child(type_verb, key, line_value)


def _get_json_diff_dict(diff_lines, key_type='root', initial_key=''):
    """Format difference lines into dictionary.

    Args:
        diff_lines (list): lines describing differences between two files
        key_type (str, optional): 'root' if key is not nested, else 'nested'.
        initial_key (str, optional): initial key for nested dict.

    Returns:
        dict: difference message as a dictionary
    """
    children = []
    line_ind = 0
    while line_ind < len(diff_lines):
        line_val = diff_lines[line_ind]
        if isinstance(diff_lines[line_ind], str):
            nested_val = diff_lines[line_ind + 1]
            ktype = 'nested'
            children.append(_get_json_diff_dict(nested_val, ktype, line_val))
            line_ind += 2
        else:
            children.append(_get_json_child(line_val))
            line_ind += 1
    return {'key': initial_key, 'type': key_type, 'children': children}


def format_json(diff_lines):
    """Format difference lines into json message.

    Args:
        diff_lines (list): lines describing differences between two files

    Returns:
        str: difference message as json string
    """
    diff_dict = _get_json_diff_dict(diff_lines)
    diff_dict.pop('key', None)
    diff_message = json.dumps(diff_dict, indent=2)
    return diff_message
