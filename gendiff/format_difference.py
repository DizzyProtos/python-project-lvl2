"""Functions for creating diff message in  different formats."""
from gendiff.formaters.diff_pretty import format_pretty
from gendiff.formaters.diff_json import format_json
from gendiff.formaters.diff_plain import format_plain


def format_diff_message(diff_lines, format_name):
    """Format diff_lines into a message of determined format.

    Args:
        diff_lines (List): difference lines from two files
        format_name (str): name of the output format

    Returns:
        str: formated difference message
    """
    if format_name == 'plain':
        return format_plain(diff_lines)
    if format_name == 'json':
        return format_json(diff_lines)
    else:
        return format_pretty(diff_lines)
