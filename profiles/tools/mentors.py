from django.db.models import Q

from django_facebook.models import FacebookCustomUser as User

from profiles.settings import ROLES, REGIONS_LABELS, AVAILABILITY_LABELS
from profiles.models import GamecoachProfile, ProfilePicture
from shared.tools import sanitize_file_field_url


def get_mentor_by_id(mentor_id):
    try:
        return GamecoachProfile.objects.get(user__username=mentor_id)
    except GamecoachProfile.DoesNotExist:
        return None


def get_mentor_by_username(username):
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


def get_all_mentors(filter_data):
    filters = generate_filters(filter_data)

    m = GamecoachProfile.objects.filter(*filters)
    print m.query

    ids = [mentor.user.id for mentor in m]
    profile_pictures_by_id = get_profile_pictures_by_ids(ids)

    mentors = []
    for i in m:
        mentor_json = i.deserialize()
        if i.user.id in profile_pictures_by_id:
            mentor_json['profile_picture'] = sanitize_file_field_url(profile_pictures_by_id[i.user.id])
        mentors.append(mentor_json)
    return mentors


def merge_filter_data(filter_data):
    availability_labels = ['day', 'time']
    avail = {}
    for label in availability_labels:
        if label in filter_data:
            avail = dict(avail.items() + filter_data[label].items())
    if not avail == {}:
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
        if not label in data or data[label] is False:
            tick = '.'
        else:
            tick = '0'
        ticks.append(tick)

    pattern = '^' + '\|'.join(ticks) + '$'

    f = {}
    f[category + "__regex"] = pattern
    return ~Q(**f)


def get_profile_pictures_by_ids(ids):
    profile_picture_entries = ProfilePicture.objects.filter(id__in=ids)
    profile_pictures_by_ids = {}
    for entry in profile_picture_entries:
        if not entry.image is None:
            profile_pictures_by_ids[entry.user.id] = entry.image.url
    return profile_pictures_by_ids
