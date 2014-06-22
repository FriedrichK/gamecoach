from django.db.models import Q

from profiles.settings import ROLES, REGIONS_LABELS, AVAILABILITY
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


def generate_filters(filter_data):
    if filter_data is None:
        return {}

    filters = []
    categories = {'roles': ROLES, 'regions': REGIONS_LABELS, 'availability': AVAILABILITY}
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
