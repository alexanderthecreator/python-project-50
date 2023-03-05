import json
import yaml


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    elif '.json' in file_path:
        return json.load(open(file_path))


def make_diff(first_dict, second_dict):
    result_diff = []
    for key in set(first_dict).union(second_dict):
        if key in first_dict and key not in second_dict:
            result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'remove'})
        if key in second_dict and key not in first_dict:
            result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'add'})
        if key in first_dict and key in second_dict:
            if first_dict[key] == second_dict[key]:
                result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'unchanged'})
            if first_dict[key] != second_dict[key]:
                if isinstance(first_dict[key], dict) and isinstance(second_dict[key], dict):
                    sub_res = (make_diff(first_dict[key], second_dict[key]))
                    if sub_res:
                        result_diff.append({'key': key, 'value': sub_res, 'meta': 'nested'})
                else:
                    result_diff.append({'key': key, 'old_value': first_dict[key], 'new_value': second_dict[key], 'meta': 'nested'})
    #print(result_diff)
    return result_diff


def format_result(result):
    sorted_result = sorted(result, key=lambda x: x["key"])
    formatted = "{\n"
    for item in sorted_result:
        key = item["key"]
        meta = item["meta"]
        value = item.get("value")
        old_value = item.get("old_value")
        new_value = item.get("new_value")
        if isinstance(value, list):
            value = format_result(value)
        if meta == "add":
            formatted += f"  + {key}: {value}\n"
        elif meta == "remove":
            formatted += f"  - {key}: {value}\n"
        elif meta == "unchanged":
            formatted += f"    {key}: {value}\n"
        elif meta == "nested":

            if isinstance(old_value, dict):
                old_value_str = format_result(make_diff(old_value, new_value))
            else:
                old_value_str = str(old_value)

            if isinstance(new_value, dict):
                new_value_str = format_result(make_diff(new_value, old_value))
            else:
                new_value_str = str(new_value)

            formatted += f"  - {key}: {old_value_str} \n"
            formatted += f"  + {key}: {new_value_str}\n"

    formatted += "}"
    print (formatted)
    return formatted


def generate_diff(file_path1, file_path2):
    """Init script for functionality tests"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    print(str_)
    return format_result(str_)


f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'


generate_diff(f_p1, f_p2)



