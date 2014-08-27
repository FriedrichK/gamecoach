import random

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
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
    social_account = create_social_account(fake, user, fake_name, fake_username)

    return user, social_account


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
    }
    user = User(**content)
    user.save()
    return user


def create_social_account(fake, user, fake_name, fake_username):
    content = {
        'user': user,
        'last_login': timezone.now(),
        'date_joined': timezone.now(),
        'provider': 'facebook',
        'uid': random.randint(0, 10000),
        'extra_data': generate_raw_data()
    }
    social_account, created = SocialAccount.objects.get_or_create(user=user)
    for key, value in content.items():
        setattr(social_account, key, value)
    social_account.save()
    return social_account


def generate_fake_username(fake_name):
    return ''.join(e for e in fake_name if e.isalnum()).lower()


def generate_raw_data():
    return {}
