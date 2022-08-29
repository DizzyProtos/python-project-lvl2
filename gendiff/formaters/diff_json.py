"""Create json difference message."""


import json


def _format_diff_json_child(type, key, line_val):
    if type == 'changed':
        value_dict = {'value1': line_val[0], 'value2': line_val[1]}
    else:
        value_dict = {'value': line_val}
    return {'key': key, 'type': type, **value_dict}


def _get_json_child(line_tuple):
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
    children = []
    line_ind = 0
    while line_ind < len(diff_lines):
        if isinstance(diff_lines[line_ind], str):
            children.append(_get_json_diff_dict(diff_lines[line_ind + 1], 'nested', diff_lines[line_ind]))
            line_ind += 2
        else:
            children.append(_get_json_child(diff_lines[line_ind]))
            line_ind += 1
    return {'key': initial_key, 'type': key_type, 'children': children}


def format_json(diff_lines):
    diff_dict = _get_json_diff_dict(diff_lines)
    diff_dict.pop('key', None)
    diff_message = json.dumps(diff_dict, indent=2)
    return diff_message
