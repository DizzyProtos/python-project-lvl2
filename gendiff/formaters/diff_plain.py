"""Format differences into a plain message."""
from gendiff.difference_description import ADD, NESTED, REMOVE, UPDATE, SAME


def _format_value(line_value):
    """Format value of a line in plain message.

    Args:
        line_value (any): value of this line

    Returns:
        str: formated string for a plain message
    """
    complex_value_str = '[complex value]'
    if isinstance(line_value, str):
        return f"'{line_value}'"
    if isinstance(line_value, dict):
        return complex_value_str
    if isinstance(line_value, bool):
        return 'true' if line_value else 'false'
    if line_value is None:
        return 'null'
    return line_value


def _format_diff_value(line_value):
    """Unpack line values and format each value

    Args:
        line_value (tuple): value from difference line.

    Returns:
        tuple: formated difference values
    """
    if isinstance(line_value, tuple):
        fv, sv = line_value
        line_value = (_format_value(fv), _format_value(sv))
    else:
        line_value = _format_value(line_value)
    return line_value


def get_plain_line(diff_type, key, line_value, parent_keys=None):
    """Format one difference line into line of plain message.

    Args:
        diff_type (str): type of change in line
        key (str): changed key
        line_value (str): value of change, one or (before, after)
        parent_keys (list, optional): keys if current line is from nested dict.

    Returns:
        str: line of the plain message
    """
    line_value = _format_diff_value(line_value)
    key = '.'.join([*parent_keys, key])

    if diff_type == UPDATE:
        from_part = f'From {line_value[0]} to {line_value[1]}'
        return f"Property '{key}' was updated. {from_part}"
    if diff_type == SAME:
        return ''
    if diff_type == ADD:
        return f"Property '{key}' was added with value: {line_value}"
    if diff_type == REMOVE:
        return f"Property '{key}' was removed"
    return ''


def format_plain(diff_lines, parent_keys=None):
    """Create plain difference message from lines.

    Args:
        diff_lines (list): lines describing differences between two files
        parent_keys (list, optional): keys of parent dicts. Defaults to None.

    Returns:
        str: plain difference message
    """
    if not parent_keys:
        parent_keys = []

    diff_message = ''
    for diff_type, key, diff_val in diff_lines:
        if diff_type == NESTED:
            diff_message += format_plain(diff_val, [*parent_keys, key])
        else:
            new_line = get_plain_line(diff_type, key, diff_val, parent_keys)
            if new_line:
                diff_message = f'{diff_message}{new_line}\n'
    if not parent_keys:
        diff_message = diff_message[:-1]
    return diff_message
