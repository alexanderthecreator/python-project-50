import json
import yaml


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    elif '.json' in file_path:
        return json.load(open(file_path))


def make_diff(first_dict, second_dict):
    """Make a diff between two dicts"""
    result_diff = []
    for key in set(first_dict).union(second_dict):
        if key in first_dict and key in second_dict:
            if type(first_dict[key]) == dict and type(second_dict[key]) == dict:
                if first_dict[key] == second_dict[key]:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'no_changes'})
                if first_dict[key] != second_dict[key]:
                    #result_diff.append({'key1': key, 'value': first_dict[key], 'meta': 'nested'})
                    #result_diff.append({'key2': key, 'value': second_dict[key], 'meta': 'nested'})
                    make_diff(first_dict[key], second_dict[key])
            else:
                if first_dict[key] == second_dict[key]:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'no_changes'})
                else:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'remove'})
                    result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'add'})
        if key in first_dict and key not in second_dict:
            result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'remove'})
        if key in second_dict and key not in first_dict:
            result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'add'})

    #print(result_diff)
    return result_diff


def stylish(str_):
    diff_string = ''
    for item in str_:
        if item['meta'] == 'no_changes':
            diff_string += f"    {item.get('key')}: {item.get('value')}\n"
        if item['meta'] == 'nested':
            diff_string += stylish (item['value'])
        if item['meta'] == 'add':
            diff_string += f"  + {item.get('key')}: {item.get('value')}\n"
        if item['meta'] == 'remove':
            diff_string += f"  - {item.get('key')}: {item.get('value')}\n"
    final_diff_string = "{\n" + diff_string.lower() + "}"
    print(final_diff_string)
    return final_diff_string


def generate_diff(file_path1, file_path2):
    """Make a string from list of diff"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    print(str_)
    return stylish(str_)




f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'


generate_diff(f_p1, f_p2)



