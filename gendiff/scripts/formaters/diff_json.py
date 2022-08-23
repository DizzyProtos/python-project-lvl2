"""Create json difference message."""


def _dict_to_json_lines(initial_key, input_dict, symb='', nest_level=1):
    """Convert dictionary into lines for diffence message.

    Args:
        initial_key (str): name of the nested dict in the parent
        input_dict (dict): dictionary to transform
        symb (str, optional): symbol to place in front of the dict name
        nest_level (str, optional): current level of nesting

    Returns:
        list: lines for a difference message
    """
    if symb:
        symb = f'{symb} '
    lines = ['{0}{1}{2}: {{'.format('\t' * nest_level, symb, initial_key)]
    for key, key_item in input_dict.items():
        if isinstance(input_dict[key], dict):
            lines += _dict_to_json_lines(key, key_item, '', nest_level + 1)
        else:
            nested_tabs = '\t' * (nest_level + 1)
            lines.append('{0}{1}: {2}'.format(nested_tabs, key, key_item))
    lines.append('{0}}}'.format('\t' * nest_level))
    return lines


def _format_diff_json_line(symb, key, line_val, nest_level):
    """Format line of json message.

    Args:
        symb (str): + or - symbol for this line
        key (any): key in the line
        line_val (any): value of the line
        nest_level (int): level of nesting for this line

    Returns:
        str: line of json message
    """
    if isinstance(line_val, dict):
        return _dict_to_json_lines(key, line_val, symb, nest_level)
    nested_tabs = '\t' * nest_level
    if symb == '':
        return ['{0}{1}: {2}'.format(nested_tabs, key, line_val)]
    return ['{0}{1} {2}: {3}'.format(nested_tabs, symb, key, line_val)]


def _get_json_line(line_tuple, nest_level=1):
    """Get json message line from difference line.

    Args:
        line_tuple (tuple): difference line (symbol, key, value)
        nest_level (int, optional): how many nested dicts are parents.

    Returns:
        str: line of json message
    """
    symb, key, line_value = line_tuple
    if symb == 'u':
        lines = _format_diff_json_line('-', key, line_value[0], nest_level)
        lines += _format_diff_json_line('+', key, line_value[1], nest_level)
    elif symb == 'e':
        lines = _format_diff_json_line('', key, line_value, nest_level)
    elif symb == 'a':
        lines = _format_diff_json_line('+', key, line_value, nest_level)
    elif symb == 's':
        lines = _format_diff_json_line('-', key, line_value, nest_level)
    else:
        lines = []
    return lines


def format_json(diff_lines, nest_level=1):
    """Create json difference message from lines.

    Args:
        diff_lines (list): lines describing differences between two files
        nest_level (int, optional): how many dicts are parents to the current.

    Returns:
        str: json difference message
    """
    nested_tabs = '\t' * nest_level
    diff_message = []
    line_ind = 0
    while line_ind < len(diff_lines):
        if isinstance(diff_lines[line_ind], str):
            diff_message.append(f'{nested_tabs}{diff_lines[line_ind]}: {{\n')
            n_value = diff_lines[line_ind + 1]
            diff_message.append(format_json(n_value, nest_level + 1))
            diff_message.append(f'{nested_tabs}}}\n')
            line_ind += 2
        elif isinstance(diff_lines[line_ind], tuple):
            formated_lines = _get_json_line(diff_lines[line_ind], nest_level)
            diff_message.append(''.join([f'{ln}\n' for ln in formated_lines]))
            line_ind += 1
    diff_message = ''.join(diff_message)
    if nest_level == 1:
        diff_message = f'{{\n{diff_message}}}'
    return diff_message
