import json
import datetime
import random
import copy

import factory
from faker import Factory
fake = Factory.create()

from django.contrib.auth.models import User

from profiles.settings import ROLES, REGIONS, AVAILABILITY, HEROES
from shared.tools import generate_res_id


def create_fake_mentors(amount):
    mentors = []
    for i in range(amount):
        fake.seed(i)
        fake_name = fake.name()
        fake_user = generate_fake_user(fake_name)
        data = {
            'user': fake_user,
            'roles': generate_random_roles(),
            'regions': generate_random_regions(),
            'availability': generate_random_availability(),
            'data': json.dumps(generate_fake_data(i, fake_name)),
            'created': datetime.datetime.now(),
            'updated': datetime.datetime.now()
        }
        mentors.append(MentorFactory(**data))
    return mentors


def generate_fake_user(fake_name):
    res_id = generate_res_id('user')
    fake_username = generate_fake_steam_id_from_fake_name(fake_name)
    email = fake_username + "@website.com"
    user = User(username=res_id, first_name=fake_name, email=email)
    user.save()
    return user


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


def generate_fake_data(seed, fake_name):
    fake.seed(seed)
    random.seed(seed)
    return {
        'description': fake.text()[:128],
        'games': random.randint(0, 1000),
        'reviews': random.randint(0, 100),
        'steamId': generate_fake_steam_id_from_fake_name(fake_name),
        'response_rate': random.random(),
        'response_time': random.randint(0, 50),
        'top_heroes': generate_top_heroes(),
        'statistics': generate_statistics()
    }


def generate_fake_steam_id_from_fake_name(fake_name):
    return ''.join(e for e in fake_name if e.isalnum()).lower()


def generate_top_heroes():
    total = random.randint(0, 5)
    heroes = []
    hero_list = copy.copy(HEROES)
    for i in range(total):
        index = random.randint(0, len(hero_list) - 1)
        heroes.append(hero_list[index])
        del hero_list[index]
    return heroes


def generate_statistics():
    return {
        'games_played': random.randint(0, 20000),
        'win_rate': random.random(),
        'solo_mmr': random.randint(0, 10000)
    }


class MentorFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = 'profiles.GamecoachProfile'
