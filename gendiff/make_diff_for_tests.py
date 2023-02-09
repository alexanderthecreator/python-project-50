import json
import yaml


def get_file(file_path):
    """Make a python object depends on file type"""
    if '.yml' or '.yaml' in file_path:
        return yaml.safe_load(open(file_path))
    elif '.json' in file_path:
        return json.load(open(file_path))


def make_diff(first_dict, second_dict, recursion_level=0):
    """Make a diff between two dicts"""
    result_diff = []
    #Итерируемся по обединенному множеству ключей 1го и 2го словарей
    for key in set(first_dict).union(second_dict):
        #Проверяем наличие ключа в обоих словарях
        if key in first_dict and key in second_dict:
            # Проверяем принадлежность значений первого и второго словаря к классу dict
            if isinstance(first_dict[key], dict) and isinstance(second_dict[key], dict):
                #Если значения по ключам - словари и они равны, то добавляем в результирующий список
                #словарь с определенными ключами, характеризующими элемент
                if first_dict[key] == second_dict[key]:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'no_changes', 'level': recursion_level})
                #Если значения по ключам - словари и они не равны, то обавляем в результирующий список
                #словари с ключами Nested для соответствующих элементов обоих словарей
                #и вызваем функцию рекурсивно для значений по текущим ключам, добавляя полученные списки в итоговый
                if first_dict[key] != second_dict[key]:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'nested', 'level': recursion_level})
                    result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'nested', 'level': recursion_level})
                    result_diff.extend(make_diff(first_dict[key], second_dict[key], recursion_level+1))
            #Обрабатываем сценарий, если оба значения по ключам - не словари (сценарий где одно из значений словарь, а другое - нет
            #даже не трогал пока, ибо и это-то не работет для вложенных словарей, а для плоских этот кусок кода рабоате олично)
            else:
                if first_dict[key] == second_dict[key]:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'no_changes', 'level': recursion_level})
                else:
                    result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'remove', 'level': recursion_level})
                    result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'add', 'level': recursion_level})
        if key in first_dict and key not in second_dict:
            result_diff.append({'key': key, 'value': first_dict[key], 'meta': 'remove', 'level': recursion_level})
        if key in second_dict and key not in first_dict:
            result_diff.append({'key': key, 'value': second_dict[key], 'meta': 'add', 'level': recursion_level})
    #print(result_diff)
    return result_diff


def stylish(str_):
    """Format result diff string"""
    diff_string = ''
    for item in str_:
        if item['meta'] == 'no_changes':
            diff_string += f"    {item.get('key')}: {item.get('value')}\n"
        if item['meta'] == 'nested':
            diff_string += f"    {item.get('key')}: {item.get('value')}\n"
        if item['meta'] == 'add':
            diff_string += f"  + {item.get('key')}: {item.get('value')}\n"
        if item['meta'] == 'remove':
            diff_string += f"  - {item.get('key')}: {item.get('value')}\n"
    final_diff_string = "{\n" + diff_string.lower() + "}"
    #print(final_diff_string)
    return final_diff_string


def generate_diff(file_path1, file_path2):
    """Init script for functionality tests"""
    first_file = get_file(file_path1)
    second_file = get_file(file_path2)
    str_ = make_diff(first_file, second_file)
    print(str_)
    return stylish(str_)


f_p1 = '/home/alexander/PycharmProjects/file4.json'
f_p2 = '/home/alexander/PycharmProjects/file5.json'


generate_diff(f_p1, f_p2)



