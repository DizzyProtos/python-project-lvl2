"""Format differences into a plain message."""
from gendiff.difference_description import ADD, REMOVE, UPDATE, SAME


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


def _unpack_diff_line(line_tuple, parent_keys=None):
    """Unpack line tuple and format value

    Args:
        line_tuple (tuple): difference line.
        parent_keys (list, optional): keys if current line is from nested dict.

    Returns:
        tuple: formated
    """
    symb, key, line_value = line_tuple
    key = '.'.join([*parent_keys, key])
    if isinstance(line_value, tuple):
        fv, sv = line_value
        line_value = (_format_value(fv), _format_value(sv))
    else:
        line_value = _format_value(line_value)
    return symb, key, line_value


def get_plain_line(line_tuple, parent_keys=None):
    """Format one difference line into line of plain message.

    Args:
        line_tuple (tuple): difference line (symbol, key, value)
        parent_keys (list, optional): keys if current line is from nested dict.

    Returns:
        str: line of the plain message
    """
    symb, key, line_value = _unpack_diff_line(line_tuple, parent_keys)

    if symb == UPDATE:
        from_part = f'From {line_value[0]} to {line_value[1]}'
        return f"Property '{key}' was updated. {from_part}"
    if symb == SAME:
        return ''
    if symb == ADD:
        return f"Property '{key}' was added with value: {line_value}"
    if symb == REMOVE:
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
    li = 0
    while li < len(diff_lines):
        if isinstance(diff_lines[li], str):
            nl = diff_lines[li + 1]
            diff_message += format_plain(nl, [*parent_keys, diff_lines[li]])
            li += 2
        else:
            new_line = get_plain_line(diff_lines[li], parent_keys)
            if new_line:
                diff_message = f'{diff_message}{new_line}\n'
            li += 1
    if not parent_keys:
        diff_message = diff_message[:-1]
    return diff_message
