"""Functions for creating diff message in  different formats."""
from gendiff.formaters.diff_pretty import format_pretty
from gendiff.formaters.diff_json import format_json
from gendiff.formaters.diff_plain import format_plain


_formaters = {'plain': format_plain,
              'json': format_json,
              'stylish': format_pretty}


def is_format_valid(format_name):
    """Check if format is implemented.

    Args:
        format_name (str): name of the format

    Returns:
        bool: True if format is implemented, False otherwise
    """
    return format_name in _formaters


def format_message(diff_lines, format_name):
    """Format diff_lines into a message of determined format.

    Args:
        diff_lines (List): difference lines from two files
        format_name (str): name of the output format

    Returns:
        str: formated difference message
    """
    return _formaters[format_name](diff_lines)
