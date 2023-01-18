import argparse
import json


def generate_diff(file_path1, file_path2):
    first_file = json.load(open(file_path1))
    second_file = json.load(open(file_path2))
    diff_string = ''
    for key in first_file.keys():
        if key in second_file:
            if first_file[key] == second_file[key]:
                diff_string += f'  {key}: {second_file[key]}\n'
            else:
                diff_string += f'- {key}: {first_file[key]}\n'
                diff_string += f'+ {key}: {second_file[key]}\n'
        else:
            diff_string += f'- {key}: {first_file[key]}\n'
    final_diff_string = "{\n" + diff_string + "}"
    print(final_diff_string)
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
