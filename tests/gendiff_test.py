from sre_parse import fix_flags
import pytest
from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    test_file1 = 'tests/fixtures/1.json'
    test_file2 = 'tests/fixtures/2.json'
    diff = generate_diff(test_file1, test_file2)
    correct_answer = '{\t-follow: False\n\thost: hexlet.io\n\t-proxy: 123.234.53.22\n\t-timeout: 50\n\t+timeout: 20\n\t+verbose: True\n}'
    assert diff == correct_answer
