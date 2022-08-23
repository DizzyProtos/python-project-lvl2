"""Functions for creating diff message in  different formats."""
from gendiff.scripts.formaters.diff_json import format_json
from gendiff.scripts.formaters.diff_plain import format_plain


def format_diff_message(diff_lines, format_name):
    """Format diff_lines into a message of determined format.

    Args:
        diff_lines (List): difference lines from two files
        format_name (str): name of the output format

    Returns:
        str: formated difference message
    """
    if format_name == 'plain':
        message = format_plain(diff_lines)
    else:
        message = format_json(diff_lines)
    return message
