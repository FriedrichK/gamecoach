from django.db.models import Q

from profiles.settings import ROLES, REGIONS_LABELS, AVAILABILITY_LABELS


def get_profile_by_id(Model, res_id):
    try:
        return Model.objects.get(user__username=res_id)
    except Model.DoesNotExist:
        return None


def get_all_profiles(Model, filter_data):
    filters = generate_filters(filter_data)

    m = Model.objects.filter(*filters)
    users = []
    for i in m:
        users.append(i.deserialize())
    return users


def merge_filter_data(filter_data):
    availability_labels = ['day', 'time']
    avail = {}
    for label in availability_labels:
        if label in filter_data:
            avail = dict(avail.items() + filter_data[label].items())
    filter_data['availability'] = avail
    return filter_data


def generate_filters(filter_data):
    print filter_data
    if filter_data is None:
        return {}

    filter_data = merge_filter_data(filter_data)

    filters = []
    categories = {'roles': ROLES, 'regions': REGIONS_LABELS, 'availability': AVAILABILITY_LABELS}
    for category, value_list in categories.items():
        if not category in filter_data:
            continue
        f = generate_filters_for_category(category, filter_data[category], value_list)
        filters.append(f)
    return filters


def generate_filters_for_category(category, data, value_list):
    ticks = []
    for label in value_list:
        if not label in data or data[label] is False:
            tick = '.'
        else:
            tick = '1'
        ticks.append(tick)

    pattern = '^' + '\|'.join(ticks) + '$'

    f = {}
    f[category + "__regex"] = pattern
    return Q(**f)
