import os
from gendiff.scripts.gendiff import generate_diff


def run_test(test_file1, test_file2, correct_file, format='json'):
    diff = generate_diff(test_file1, test_file2, format)
    with open('temp_difference.txt', 'w') as f:
        f.write(diff)

    with open('temp_difference.txt', 'r') as f:
        answer = f.read()
    with open(correct_file, 'r') as f:
        correct_answer = f.read()
    assert answer == correct_answer
    os.remove('temp_difference.txt')


def test_gendiff_json():
    test_file1 = 'tests/fixtures/1.json'
    test_file2 = 'tests/fixtures/2.json'
    correct_file = 'tests/fixtures/correct.txt'
    run_test(test_file1, test_file2, correct_file, 'json')


def test_gendiff_yaml():
    test_file1 = 'tests/fixtures/1.yaml'
    test_file2 = 'tests/fixtures/2.yaml'
    correct_file = 'tests/fixtures/correct.txt'
    run_test(test_file1, test_file2, correct_file, 'json')


def test_gendiff_json_plain():
    test_file1 = 'tests/fixtures/1.json'
    test_file2 = 'tests/fixtures/2.json'
    correct_file = 'tests/fixtures/correct_plain.txt'
    run_test(test_file1, test_file2, correct_file, 'plain')


def test_gendiff_yaml_plain():
    test_file1 = 'tests/fixtures/1.yaml'
    test_file2 = 'tests/fixtures/2.yaml'
    correct_file = 'tests/fixtures/correct_plain.txt'
    run_test(test_file1, test_file2, correct_file, 'plain')


