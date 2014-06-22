from django.db.models import Q

from profiles.settings import ROLES, REGIONS_LABELS, AVAILABILITY_LABELS
from profiles.models import GamecoachProfile
from profiles.tools.fake import create_fake_users


def get_all_mentors(filter_data):
    filters = generate_filters(filter_data)

    test = GamecoachProfile.objects.all()
    if len(test) == 0:
        create_fake_users(100)

    m = GamecoachProfile.objects.filter(*filters)
    mentors = []
    for i in m:
        mentors.append(i.deserialize())
    return mentors


def merge_filter_data(filter_data):
    availability_labels = ['day', 'time']
    avail = {}
    for label in availability_labels:
        if label in filter_data:
            avail = dict(avail.items() + filter_data[label].items())
    filter_data['availability'] = avail
    return filter_data


def generate_filters(filter_data):
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
        print "X", label, data
        if not label in data or data[label] is False:
            tick = '.'
        else:
            tick = '1'
        ticks.append(tick)

    pattern = '^' + '\|'.join(ticks) + '$'
    print category, pattern

    f = {}
    f[category + "__regex"] = pattern
    return Q(**f)
