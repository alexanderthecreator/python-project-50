import json
import yaml


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    elif '.json' in file_path:
        return json.load(open(file_path))


#list_of_dicts = []
def make_diff(first_dict, second_dict):
    """Make a diff between two dicts"""
    diff_ = set(first_dict) | set(second_dict)
    # print(diff_)
    list_of_dicts = []
    for item in diff_:
        if item in first_dict and item in second_dict:
            if type(first_dict[item]) == dict and type(second_dict[item]) == dict and first_dict[item] != second_dict[item]:
                list_of_dicts.append({'key': item, 'item': first_dict[item], 'meta': 'nested'})
            elif type(first_dict[item]) == dict and type(second_dict[item]) == dict and first_dict[item] == second_dict[item]:
                list_of_dicts.append({'key': item, 'item': first_dict[item], 'meta': 'no_changes'})
            else:
                list_of_dicts.append({'key': item, 'item': first_dict[item], 'meta': 'remove'})
                list_of_dicts.append({'key': item, 'item': second_dict[item], 'meta': 'add'})
        elif item in first_dict and item not in second_dict:
            list_of_dicts.append({'key': item, 'item': first_dict[item], 'meta': 'remove'})
        elif item in second_dict and item not in first_dict:
            list_of_dicts.append({'key': item, 'item': first_dict[item], 'meta': 'add'})
        if type(first_dict.get(item)) == dict and type(second_dict.get(item)) == dict:
            list_of_dicts.extend(make_diff(first_dict[item], second_dict[item]))
    #print(list_of_dicts)
    return list_of_dicts


def generate_diff(file_path1, file_path2):
    """Make a string from list of diff"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    diff_string = ''
    for item in make_diff(first_file, second_file):
        for key in item:
            if key == 'meta':
                break
            elif item['meta'] == 'no_changes':
                diff_string += f"    {item.get('key')}: {item.get('value')}\n"
            elif item['meta'] == 'nested':
                diff_string += f"    {item.get('key')}: {item.get('value')}\n"
            elif item['meta'] == 'add':
                diff_string += f"  + {item.get('key')}: {item.get('value')}\n"
            elif item['meta'] == 'remove':
                diff_string += f"  - {item.get('key')}: {item.get('value')}\n"
    final_diff_string = "{\n" + diff_string.lower() + "}"
    #print(final_diff_string)
    return final_diff_string


f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'
generate_diff(f_p1, f_p2)


