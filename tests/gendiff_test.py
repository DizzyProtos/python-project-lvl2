import json
import pytest
from gendiff import generate_diff


TEST_FILES = {
    'json': ['tests/fixtures/1.json', 'tests/fixtures/2.json'],
    'yaml': ['tests/fixtures/1.yaml', 'tests/fixtures/2.yaml']
}


TEST_FORMATS = {'stylish': 'tests/fixtures/correct.txt',
                'plain': 'tests/fixtures/correct_plain.txt',
                'json': 'tests/fixtures/correct_json.txt'}


@pytest.fixture(params=TEST_FILES)
def test_files(request):
    return TEST_FILES[request.param]


@pytest.fixture(params=TEST_FORMATS)
def test_formats(request):
    return request.param, TEST_FORMATS[request.param]


def test_gendiff(test_files, test_formats):
    test_file1, test_file2 = test_files
    message_format, correct_file = test_formats
    with open(correct_file, 'r') as f:
        correct_answer = f.read()
    assert generate_diff(test_file1, test_file2, message_format) == correct_answer
