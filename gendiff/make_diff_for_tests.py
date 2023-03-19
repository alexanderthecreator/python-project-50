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
            result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'removed'})
        if key in second_dict and key not in first_dict:
            result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'added'})
        if key in first_dict and key in second_dict:
            if first_dict[key] == second_dict[key]:
                result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'unchanged'})
            else:
                if isinstance(first_dict[key], dict) and isinstance(second_dict[key], dict):
                    sub_res = (make_diff(first_dict[key], second_dict[key]))
                    if sub_res:
                        result_diff.append({'key': key, 'value': sub_res, 'meta': 'nested'})
                else:
                    result_diff.append({'key': key, 'value': (first_dict[key], second_dict[key]), 'meta': 'changed'})
    return result_diff


def format_diff(result_diff, indent=1):
    """
    Generate a formatted string representation of the differences between two nested dictionaries
    based on the meta information generated by the compare_dicts function.
    """
    sorted_result = sorted(result_diff, key=lambda x: x["key"])
    result = "{"
    for diff in sorted_result:
        meta, key, value = diff["meta"], diff["key"], diff["value"]
        if meta == "added":
            result += f"\n{'    ' * indent}+ {key}: {format_value(value, indent + 1)}"
        elif meta == "removed":
            result += f"\n{'    ' * indent}- {key}: {format_value(value, indent + 1)}"
        elif meta == "changed":
            result += f"\n{'    ' * indent}- {key}: {format_value(value[0], indent + 1)}"
            result += f"\n{'    ' * indent}+ {key}: {format_value(value[1], indent + 1)}"
        elif meta == "unchanged":
            result += f"\n{'    ' * (indent)}{key}: {format_value(value, indent + 1)}"
        elif meta == "nested":
            result += f"\n{'    ' * (indent)} {key}: {format_diff(value, indent + 1)}"
    result +=  "\n}"
    #print(sorted_result)
    return result


def format_value(value, indent):
    if isinstance(value, dict):
        for k, v in value.items():
            substring = f"\n{'    ' * indent} {k}: {v}"
            subres = "{" + substring + "\n" + "   "*indent + "}"
            return subres
    elif isinstance(value, str):
        return f"{value}"
    else:
        return str(value)


def generate_diff(file_path1, file_path2):
    """Init script for functionality tests"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    comp = format_diff(str_)
    print(comp)
    return comp


f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'

'''f_p1 = '/tests/fixtures/file1.json'
f_p2 = '/tests/fixtures/file1.json'''





generate_diff(f_p1, f_p2)



