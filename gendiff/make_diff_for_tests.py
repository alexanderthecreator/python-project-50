import json
import yaml
import os


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path, 'r'))
    elif '.json' in file_path:
        return json.load(open(file_path, 'r'))


def make_diff(first_dict, second_dict):
    """
    Generate a diff between two nested dictionaries
    """
    result_diff = []
    parrent_key = ''
    for key in set(first_dict).union(second_dict):
        if key in first_dict and key not in second_dict:
            result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'removed', 'path': f'{parrent_key}.{key}'})
        if key in second_dict and key not in first_dict:
            result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'added', 'path': f'{parrent_key}.{key}'})
        if key in first_dict and key in second_dict:
            if first_dict[key] == second_dict[key]:
                result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'unchanged', 'path': f'{parrent_key}.{key}'})
            else:
                if isinstance(first_dict[key], dict) and isinstance(second_dict[key], dict):
                    sub_res = (make_diff(first_dict[key], second_dict[key]))
                    if sub_res:
                        result_diff.append({'key': key, 'value': sub_res, 'meta': 'nested', 'path': f'{parrent_key}.{key}'})
                else:
                    result_diff.append({'key': key, 'value': (first_dict[key], second_dict[key]), 'meta': 'changed', 'path': f'{parrent_key}.{key}'})
    return result_diff


TABULATION = " " * 4


def format_diff(result_diff, indent=1):
    sorted_result = sorted(result_diff, key=lambda x: x["key"])
    result = "{"
    for diff in sorted_result:
        meta, key, value, path = diff["meta"], diff["key"], diff["value"], diff["path"]
        if meta == "added":
            result += f"\n{TABULATION * (indent-1)}  + {key}: {format_value(value, indent)}"
        elif meta == "removed":
            result += f"\n{TABULATION * (indent-1)}  - {key}: {format_value(value, indent)}"
        elif meta == "changed":
            result += f"\n{TABULATION * (indent-1)}  - {key}: {format_value(value[0], indent)}"
            result += f"\n{TABULATION * (indent-1)}  + {key}: {format_value(value[1], indent)}"
        elif meta == "unchanged":
            result += f"\n{TABULATION * (indent)}{key}: {format_value(value, indent)}"
        elif meta == "nested":
            result += f"\n{'    ' * (indent-1)}    {key}: {format_diff(value, indent + 1)}"
    result +=  f"\n{TABULATION * (indent - 1)}" + "}"
    return result


def format_value(value, indent):
    if isinstance(value, dict):
        sub_res = []
        for k, v in value.items():
            if isinstance(v, dict):
                sub_res.append(f"{TABULATION * (indent+1)}{k}: {format_value(v, indent + 1)}")
            else:
                sub_res.append(f"{TABULATION * (indent+1)}{k}: {v}")
        return "{\n" + "\n".join(sub_res) + f"\n{TABULATION * indent}" + "}"
    else:
        if value == True:
            value = 'true'
            return value
        elif value == None:
            value = 'null'
            return value
        else:
            return str(value)


def format_diff_plain(result_diff):
    sorted_result = sorted(result_diff, key=lambda x: x["key"])
    result = ""
    for diff in sorted_result:
        meta, key, value, path = diff["meta"], diff["key"], diff["value"], diff["path"]
        if meta == "added":
            result += f"Property '{path}' was added with value: '{format_value_plain(value)}'\n"
        elif meta == "removed":
            result += f"Property '{path}' was removed\n"
        elif meta == "changed":
            result += f"Property '{path}' was updated. From '{format_value_plain(value[0])}' to '{format_value_plain(value[1])}'\n"
        elif meta == "nested":
            result += f"{format_diff_plain(value)}"
    return result


def format_value_plain(value):
    if isinstance(value, dict):
        sub_res = []
        for k, v in value.items():
            if isinstance(v, dict):
                return "[Complex value]"
    else:
        if value == True:
            value = 'true'
            return value
        elif value == None:
            value = 'null'
            return value
        elif value == False:
            value = 'false'
            return value
        else:
            return str(value)




def generate_diff(file_path1, file_path2):
    """Init script for functionality tests"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    comp = format_diff_plain(str_)
    print(comp)
    return comp

#print(os.getcwd())

"""f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'"""

f_p1 = './fixtures/file4.json'
f_p2 = './fixtures/file5.json'



generate_diff(f_p1, f_p2)



