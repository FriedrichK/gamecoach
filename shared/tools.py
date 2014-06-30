import datetime
import random


def generate_res_id(prefix='none'):
    return prefix + generate_date_part() + generate_random_string(6)


def generate_date_part():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def generate_random_string(length):
    valid = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    text = ''
    for i in range(length):
        index = random.randint(0, len(valid) - 1)
        text += valid[index]
    return text


def serialize_datetime(dt):
    return {
        'year': dt.year,
        'month': dt.month,
        'day': dt.day,
        'hour': dt.timetuple().tm_hour,
        'minute': dt.timetuple().tm_min,
        'second': dt.timetuple().tm_sec,
    }


def check_request_requirements(request, request_type, list_of_required_variables):
    for variable in list_of_required_variables:
        req = getattr(request, request_type)
        if not variable in req:
            return False
    return True
