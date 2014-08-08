import random
import json
import copy

from django.utils import timezone

from profiles.settings import ROLES, REGIONS, AVAILABILITY, HEROES
from profiles.models import GamecoachProfile

from faker import Faker


def create_mentor_profile(user, profile, is_mentor=True):
    return create_profile(user, profile, GamecoachProfile, is_mentor)


def create_profile(user, profile, Model, is_mentor=True):
    content = {
        'user': user,
        'username': user.username,
        'roles': generate_random_roles(),
        'regions': generate_random_regions(),
        'availability': generate_random_availability(),
        'data': json.dumps(generate_fake_data(user)),
        'created': timezone.now(),
        'updated': timezone.now(),
        'is_mentor': is_mentor
    }
    model = Model(**content)
    model.save()
    return model


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


def generate_fake_data(user):
    fake = Faker()
    return {
        'description': fake.text()[:128],
        'games': random.randint(0, 1000),
        'reviews': random.randint(0, 100),
        'steamId': user.username,
        'response_rate': random.random(),
        'response_time': random.randint(0, 50),
        'top_heroes': generate_top_heroes(),
        'statistics': generate_statistics()
    }


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
