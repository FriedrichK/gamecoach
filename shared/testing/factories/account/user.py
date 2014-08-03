import random
from datetime import datetime, date

from django_facebook.models import FacebookCustomUser as User
from django_facebook.models import FacebookProfile as Profile
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from faker import Faker

TEST_PASSWORD = 'test'


def create_user(is_superuser=False, is_staff=False, is_active=True):
    seed = random.randint(0, 1000000000)
    fake = Faker()
    fake.seed(seed)

    fake_first_name = fake.first_name()
    fake_last_name = fake.last_name()
    fake_name = '%s %s' % (fake_first_name, fake_last_name)
    fake_username = generate_fake_username(fake_name)

    user = create_custom_user(fake_first_name, fake_last_name, fake_name, fake_username, is_superuser, is_staff, is_active)
    profile = create_profile(fake, user, fake_name, fake_username)

    return user, profile


def create_custom_user(fake_first_name, fake_last_name, fake_name, fake_username, is_superuser, is_staff, is_active):
    content = {
        'password': make_password(TEST_PASSWORD),
        'last_login': timezone.now(),
        'is_superuser': is_superuser,
        'username': fake_username,
        'first_name': fake_first_name,
        'last_name': fake_last_name,
        'email': '%s@test.com' % (fake_username),
        'is_staff': is_staff,
        'is_active': is_active,
        'date_joined': timezone.now(),
        'about_me': None,
        'facebook_id': None,
        'access_token': None,
        'facebook_name': None,
        'facebook_profile_url': None,
        'website_url': None,
        'blog_url': None,
        'date_of_birth': None,
        'gender': None,
        'raw_data': None,
        'facebook_open_graph': None,
        'new_token_required': False,
        'image': '',
        'state': None
    }
    user = User(**content)
    user.save()
    return user


def create_profile(fake, user, fake_name, fake_username):
    content = {
        'about_me': fake.text(max_nb_chars=100),
        'facebook_id': random.randint(1000000000, 10000000000),
        'access_token': fake.password(),
        'facebook_name': fake_name,
        'facebook_profile_url': 'https://www.facebook.com/%s' % fake_username,
        'website_url': None,
        'blog_url': None,
        'date_of_birth': random_date_of_birth(),
        'raw_data': generate_raw_data(),
        'facebook_open_graph': None,
        'new_token_required': False,
        'image': 'images/facebook_profiles/%s.jpg' % (fake_username),
        'user': user
    }
    profile, created = Profile.objects.get_or_create(user=user)
    for key, value in content.items():
        setattr(profile, key, value)
    profile.save()
    return profile


def generate_fake_username(fake_name):
    return ''.join(e for e in fake_name if e.isalnum()).lower()


def generate_raw_data():
    return {}


def random_date_of_birth():
    year = random.randint(1960, 1990)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return date(year, month, day)


def random_gender():
    result = random.random()
    if result > 0.5:
        return 'f'
    return 'm'
