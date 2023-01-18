import pytest

from gendiff.scripts.gendiff import generate_diff


@pytest.fixture()
def get_test_jsons():
    """Get two JSON files address"""
    first_file_address = '/home/alexander/PycharmProjects/file1.json'
    second_file_address = '/home/alexander/PycharmProjects/file2.json'
    return first_file_address, second_file_address


def test_generate_diff(get_test_jsons):
    assert generate_diff(*get_test_jsons) == '{\n  host: hexlet.io\n- timeout: 50\n+ timeout: 20\n- proxy: ' \
                                            '123.234.53.22\n- follow: False\n}'
