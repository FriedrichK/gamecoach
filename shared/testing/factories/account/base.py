from user import create_user

from shared.testing.factories.account.profile import create_student_profile, create_mentor_profile


def create_accounts(number, is_user=True, is_mentor=False, is_superuser=False, is_staff=False, is_active=True):
    accounts = []
    for i in range(number):
        accounts.append(create_account(is_user, is_mentor, is_superuser, is_staff, is_active))
    return accounts


def create_account(is_user=True, is_mentor=False, is_superuser=False, is_staff=False, is_active=True):
    if is_user is False and is_mentor is False:
        raise CreateAccountException('cannot create accounts which are neither users nor mentors')

    entries = {}
    user, profile = create_user(is_superuser, is_staff, is_active)
    entries['user'] = user
    entries['profile'] = profile
    entries['profiles'] = {}

    if is_user:
        entries['profiles']['student'] = create_student_profile(user, profile)

    if is_mentor:
        entries['profiles']['mentor'] = create_mentor_profile(user, profile)

    return entries


class CreateAccountException(Exception):
    pass
