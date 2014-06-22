import datetime
import random
import json
import re

from django.db.models import Q

import factory
from faker import Factory
fake = Factory.create()

from profiles.settings import ROLES, REGIONS, REGIONS_LABELS, AVAILABILITY
from profiles.models import GamecoachProfile


def get_all_mentors(filter_data):
    filters = generate_filters(filter_data)

    test = GamecoachProfile.objects.all()
    if len(test) == 0:
        create_fake_users(100)

    m = GamecoachProfile.objects.filter(*filters)
    print GamecoachProfile.objects.filter(*filters).query
    print "mentors found", len(m)
    mentors = []
    for i in m:
        mentors.append(i.deserialize())
    return mentors


def create_fake_users(amount):
    mentors = []
    for i in range(amount):
        data = {
            'roles': generate_random_roles(),
            'regions': generate_random_regions(),
            'availability': generate_random_availability(),
            'data': json.dumps(generate_fake_data()),
            'created': datetime.datetime.now(),
            'updated': datetime.datetime.now()
        }
        mentors.append(MentorFactory(**data))
    return mentors


def generate_random_roles():
    return generate_random_stringified_binary_list(ROLES)


def generate_random_regions():
    return generate_random_stringified_binary_list(REGIONS)


def generate_random_availability():
    return generate_random_stringified_binary_list(AVAILABILITY)


def generate_random_stringified_binary_list(options):
    values = []
    for i in range(len(options)):
        rnd = random.random()
        val = 1 if rnd > 0.5 else 0
        values.append(str(val))
    return '|'.join(values)


def generate_fake_data():
    return {
        'name': fake.name(),
        'description': fake.text()[:128],
        'games': random.randint(0, 1000),
        'reviews': random.randint(0, 100)
    }


class MentorFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'profiles.GamecoachProfile'


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
