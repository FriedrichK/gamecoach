import json

from profiles.settings import ROLES, REGIONS, AVAILABILITY


def deserialize_data(input_string):
    if input_string is None:
        return {}
    return json.loads(input_string)


def deserialize_roles(input_string):
    return deserialize_string_storage(input_string, ROLES)


def deserialize_regions(input_string):
    return deserialize_string_storage(input_string, REGIONS)


def deserialize_availability(input_string):
    return deserialize_string_storage(input_string, AVAILABILITY)


def deserialize_string_storage(input_string, value_list):
    if input_string is None:
        return {}
    items = tokenize_input_string(input_string)
    return map_items_to_data(items, value_list)


def map_items_to_data(items, value_list):
    data = {}
    for i in range(len(items)):
        label = get_label_from_value_list(value_list, i)
        value = get_value_from_item(items[i])
        if not label is None or value is None:
            data[label] = value
    return data


def tokenize_input_string(input_string):
    return input_string.split('|')


def get_label_from_value_list(value_list, index):
    if index >= len(value_list):
        return None
    return value_list[index]


def get_value_from_item(item):
    if item == '0':
        return False
    if item == '1':
        return True
    return None


def deserialize_date(dt):
    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.timetuple().tm_hour,
        'minute': dt.timetuple().tm_min,
        'second': dt.timetuple().tm_sec,
    }
