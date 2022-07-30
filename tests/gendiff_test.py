from sre_parse import fix_flags
import os
from gendiff.scripts.gendiff import generate_diff


def test_gendiff():
    test_file1 = 'tests/fixtures/1.json'
    test_file2 = 'tests/fixtures/2.json'
    diff = generate_diff(test_file1, test_file2)
    with open('temp_difference.txt', 'w') as f:
        f.write(diff)

    with open('temp_difference.txt', 'r') as f:
        answer = f.read()
    with open(r'tests/fixtures/correct.txt', 'r') as f:
        correct_answer = f.read()
    assert answer == correct_answer
    os.remove('temp_difference.txt')
