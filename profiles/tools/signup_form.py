import datetime
import json
import re

from profiles.settings import SIGNUP_FORM
from profiles.models import GamecoachProfile
from profiles.tools.serialization import serialize_roles, serialize_regions, serialize_mentoring, serialize_availability
from profiles.settings import HEROES_HASH

WIN_RATE_REGEX_PATTERN = re.compile('([0-9\\.]+)')


def add_profile_for_user(user, form):
    profile = build_profile_from_signup_form_data(form)
    setattr(profile, 'user', user)
    return profile.save()


def update_profile_for_user(user, form):
    profile = user.gamecoachprofile
    model_data = generate_form_data(form)
    for label, value in model_data.items():
        setattr(profile, label, value)
    return profile.save()


def get_mentor_signup_form_from_request(data):
    form_content = {}
    for key, value in SIGNUP_FORM.items():
        item = None
        if key in data:
            item = data[key]
        form_content[key] = item
    return form_content


def build_profile_from_signup_form_data(signup_form_data):
    model_data = generate_form_data(signup_form_data)
    return GamecoachProfile(**model_data)


def generate_form_data(signup_form_data):
    return {
        'username': signup_form_data['displayName'],
        'email': signup_form_data['email'],
        'roles': serialize_roles(get_hash(signup_form_data, 'role')),
        'regions': serialize_regions(get_hash(signup_form_data, 'region')),
        'mentoring': serialize_mentoring(get_hash(signup_form_data, 'mentoring')),
        'availability': serialize_availability(get_hash(signup_form_data, 'day'), get_hash(signup_form_data, 'time')),
        'data': json.dumps(generate_form_data_data(signup_form_data)),
        'created': datetime.datetime.now(),
        'updated': datetime.datetime.now()
    }


def generate_form_data_data(signup_form_data):
    return {
        'description': signup_form_data['about'],
        'games': 0,
        'reviews': 0,
        'steamId': signup_form_data['steamId'],
        'steamIdLink': signup_form_data['steamIdLink'],
        'response_rate': None,
        'response_time': None,
        'top_heroes': generate_top_heroes(get_data(signup_form_data, 'topheroes', {})),
        'statistics': json.dumps(generate_statistics(signup_form_data)),
    }


def generate_statistics(signup_form_data):
    return {
        'games_played': get_statistic(signup_form_data, 'gamesPlayed'),
        'win_rate': clean_win_rate(get_statistic(signup_form_data, 'winRate')),
        'solo_mmr': get_statistic(signup_form_data, 'soloMmr')
    }


def clean_win_rate(input):
    if input is None:
        return None
    r = WIN_RATE_REGEX_PATTERN.search(input)
    if r is None:
        return None
    groups = r.groups()
    if len(groups) < 1:
        return None
    rate_as_percent = float(groups[0])
    return rate_as_percent / 100.0


def generate_top_heroes(data):
    hero_names = []
    hero_list = generate_hero_list_from_hash(data)
    for hero_label in hero_list:
        hero_name = get_hero_name_for_hero_label(hero_label)
        if not hero_name is None:
            hero_names.append(hero_name)
    return hero_names


def generate_hero_list_from_hash(data):
    hero_list = []
    indices = ['first', 'second', 'third']
    for index in indices:
        if index in data:
            hero_list.append(data[index])
    return hero_list


def get_hero_name_for_hero_label(hero_label):
    if hero_label in HEROES_HASH:
        return HEROES_HASH[hero_label]
    return None


def get_data(signup_form_data, label, default=None):
    if signup_form_data is None or not label in signup_form_data:
        return default
    return signup_form_data[label]


def get_statistic(signup_form_data, label, default=None):
    if signup_form_data is None:
        return default
    if not 'statistics' in signup_form_data:
        return default
    if not label in signup_form_data['statistics']:
        return default
    return signup_form_data['statistics'][label]


def get_hash(src, label):
    if src is None or not label in src:
        return None
    return src[label]
