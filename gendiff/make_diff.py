def make_diff(first_dict, second_dict):
    """
    Generate a diff between two nested dictionaries
    """
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
