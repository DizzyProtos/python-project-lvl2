"""Create json difference message."""
import json


from gendiff.difference_description import ADD, NESTED, REMOVE, UPDATE, SAME


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


def _get_json_child(symb, key, line_value):
    """Get difference dict for a single line.

    Args:
        diff_type (str): type of change in a line
        key (str): changed key
        line_value (str): value of change, one value or (before, after)

    Returns:
        dict: difference as a dictionary
    """
    type_verb = ''
    if symb == UPDATE:
        type_verb = 'changed'
    if symb == SAME:
        type_verb = 'unchanged'
    if symb == ADD:
        type_verb = 'added'
    if symb == REMOVE:
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
    for diff_type, key, diff_val in diff_lines:
        if diff_type == NESTED:
            ktype = 'nested'
            children.append(_get_json_diff_dict(diff_val, ktype, key))
        else:
            children.append(_get_json_child(diff_type, key, diff_val))
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
