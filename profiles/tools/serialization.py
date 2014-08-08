import json

from profiles.settings import ROLES, REGIONS, REGIONS_LABELS, MENTORING, MENTORING_LABELS, AVAILABILITY


def serialize_data(data_hash):
    return json.dumps(data_hash)


def deserialize_data(input_string):
    if input_string is None:
        return {}
    data = json.loads(input_string)
    data['statistics']
    return data


def serialize_roles(data_hash):
    return serialize_string_storage(data_hash, ROLES)


def deserialize_roles(input_string):
    return deserialize_string_storage(input_string, ROLES)


def serialize_regions(data_hash):
    return serialize_string_storage(data_hash, REGIONS_LABELS)


def deserialize_regions(input_string):
    return deserialize_string_storage(input_string, REGIONS_LABELS)


def serialize_mentoring(input_string):
    return serialize_string_storage(input_string, MENTORING)


def deserialize_mentoring(input_string):
    return deserialize_string_storage(input_string, MENTORING)


def serialize_availability(day, time):
    tokens = []
    if day == "1":
        tokens += ["1", "0"]
    if day == "2":
        tokens += ["0", "1"]
    if time == "1":
        tokens += ["1", "0"]
    if time == "2":
        tokens += ["0", "1"]
    return "|".join(tokens)


def deserialize_availability(input_string):
    return deserialize_string_storage(input_string, AVAILABILITY)


def serialize_string_storage(data_hash, value_list):
    if data_hash is None or data_hash == {}:
        return None
    return build_data_string(data_hash, value_list)


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


def build_data_string(data_hash, value_list):
    tokens = []
    for item in value_list:
        token = '0'
        if item in data_hash and data_hash[item] is True:
            token = '1'
        tokens.append(token)
    return '|'.join(tokens)


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
