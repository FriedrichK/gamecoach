import datetime
import random
import json

import factory
from faker import Factory
fake = Factory.create()

from profiles.settings import ROLES, REGIONS, AVAILABILITY
from profiles.models import GamecoachProfile


def get_all_mentors():
    m = GamecoachProfile.objects.all()
    if len(m) == 0:
        m = create_fake_users(100)

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
