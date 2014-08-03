from user import create_user

from shared.testing.factories.account.profile import create_mentor_profile


def create_accounts(number, is_superuser=False, is_staff=False, is_active=True):
    accounts = []
    for i in range(number):
        accounts.append(create_account(is_superuser, is_staff, is_active))
    return accounts


def create_account(is_superuser=False, is_staff=False, is_active=True):
    entries = {}
    user, profile = create_user(is_superuser, is_staff, is_active)
    entries['user'] = user
    entries['profile'] = profile
    entries['profiles'] = {}

    entries['profiles']['mentor'] = create_mentor_profile(user, profile)

    return entries


class CreateAccountException(Exception):
    pass
