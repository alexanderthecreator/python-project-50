import pytest

from gendiff.scripts.gendiff import generate_diff


@pytest.fixture()
def get_test_jsons():
    """Get two JSON files address"""
    first_file_address = './fixtures/file1.json'
    second_file_address = './fixtures/file2.json'
    return first_file_address, second_file_address


def test_generate_diff(get_test_jsons):
    f = open('./fixtures/result_string.txt')
    assert generate_diff(*get_test_jsons) == f.read()
