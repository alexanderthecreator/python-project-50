import json
import yaml


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    elif '.json' in file_path:
        return json.load(open(file_path))


'''def make_diff(first_file, second_file):
    first_file_keys = set(zip(first_file.keys(), first_file.values()))
    second_file_keys = set(zip(second_file.keys(), second_file.values()))
    list1 = [{key: value, 'meta': 'no_changes'} for key, value in first_file.items() if
             (key, value) in first_file_keys & second_file_keys]
    list2 = [{key: value, 'meta': 'remove'} for key, value in first_file.items() if
             (key, value) in first_file_keys - second_file_keys]
    list3 = [{key: value, 'meta': 'add'} for key, value in first_file.items() if
             (key, value) in second_file_keys - first_file_keys]
    result_list = list1 + list2 + list3
    return result_list'''


def make_diff(first_file, second_file):
    """Make a diff between two dicts"""
    diff_ = set(first_file) | set(second_file)
    # print(diff_)
    list_of_dicts = []
    for item in diff_:
        if item in first_file and item in second_file:
            if first_file[item] == second_file[item]:
                list_of_dicts.append({item: first_file[item], 'meta': 'no_changes'})
            else:
                list_of_dicts.append({item: first_file[item], 'meta': 'remove'})
                list_of_dicts.append({item: second_file[item], 'meta': 'add'})
        if item in first_file and item not in second_file:
            list_of_dicts.append({item: first_file[item], 'meta': 'remove'})
        if item in second_file and item not in first_file:
            list_of_dicts.append({item: second_file[item], 'meta': 'add'})
        if type(first_file.get(item)) == dict and type(second_file.get(item)) == dict:
            make_diff(first_file[item], second_file[item])
    print(list_of_dicts)
    return list_of_dicts


def generate_diff(file_path1, file_path2):
    """Make a string from list of diff"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    list_ = make_diff(first_file, second_file)
    diff_string = ''
    for item in list_:
        for key in item:
            if key == 'meta':
                break
            elif item['meta'] == 'no_changes':
                diff_string += f'    {key}: {item[key]}\n'
            elif item['meta'] == 'add':
                diff_string += f'  + {key}: {item[key]}\n'
            elif item['meta'] == 'remove':
                diff_string += f'  - {key}: {item[key]}\n'
    final_diff_string = "{\n" + diff_string.lower() + "}"
    #print(final_diff_string)
    return final_diff_string


f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'
generate_diff(f_p1, f_p2)


