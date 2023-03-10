import argparse
import json
import yaml


def get_file(file_path):
    if '.yml' or '.yaml' in file_path:
        file = yaml.safe_load(open(file_path))
        return file
    elif '.json' in file_path:
        file = json.load(open(file_path))
        return file


def generate_diff(file_path1, file_path2):
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    diff_string = ''
    for key in first_file.keys():
        if key in second_file:
            if first_file[key] == second_file[key]:
                diff_string += f'    {key}: {second_file[key]}\n'
            else:
                diff_string += f'  - {key}: {first_file[key]}\n'
                diff_string += f'  + {key}: {second_file[key]}\n'
        else:
            diff_string += f'  - {key}: {first_file[key]}\n'
    for key in second_file.keys():
        if key not in first_file:
            diff_string += f'  + {key}: {second_file[key]}\n'
    final_diff_string = "{\n" + diff_string + "}"
    print(final_diff_string)
    print(type(first_file))
    return final_diff_string


def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('file_path1')
    parser.add_argument('file_path2')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    generate_diff(args.file_path1, args.file_path2)


if __name__ == "__main__":
    main()
