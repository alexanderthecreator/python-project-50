import argparse
import json
import yaml
from gendiff_.make_diff import make_diff
from gendiff_.formatter import format_diff


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    if '.json' in file_path:
        return json.load(open(file_path))


def generate_diff(file_path1, file_path2):
    """Init script for functionality tests"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    comp = format_diff(str_)
    print(comp)
    return comp


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('file_path1')
    parser.add_argument('file_path2')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    generate_diff(args.file_path1, args.file_path2)


if __name__ == "__main__":
    main()
