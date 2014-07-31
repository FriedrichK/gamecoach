from django.test import TestCase

from django_facebook.models import FacebookCustomUser as User

#from shared.testing.factories.account import create_accounts
from profiles.models import GamecoachProfile
from profiles.settings import ROLES, REGIONS_LABELS
from profiles.tools.mentors import get_all_mentors


class ToolsMentorsTestCase(TestCase):

    def setUp(self):
        self._profiles = create_mock_profiles()

    def test_returns_expected_result_with_all_role_filters_untrue(self):
        filter_data = {
            'roles': {
                'carry': False
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 3)

    def test_returns_expected_result_for_role_shared_by_all(self):
        filter_data = {
            'roles': {
                'carry': True
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 3)

    def test_returns_expected_result_for_role_shared_by_two(self):
        filter_data = {
            'roles': {
                'ganker': True
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 2)

    def test_returns_expected_result_for_multiple_roles(self):
        filter_data = {
            'roles': {
                'ganker': True,
                'disabler': True
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 3)

    def test_returns_expected_reuslt_for_single_region(self):
        filter_data = {
            'regions': {
                'euwest': True,
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 1)

    def test_returns_expected_reuslt_for_three_regions(self):
        filter_data = {
            'regions': {
                'seasia': True,
                'russia': True,
                'australia': True
            }
        }
        actual = get_all_mentors(filter_data)

        self.assertEqual(len(actual), 3)


def create_mock_profiles():
    profiles = []
    data = [
        {'roles': {'carry': True, 'ganker': True}, 'regions': {'euwest': True, 'seasia': True}},
        {'roles': {'carry': True, 'ganker': True}, 'regions': {'eueast': True, 'russia': True}},
        {'roles': {'carry': True, 'disabler': True}, 'regions': {'eueast': True, 'australia': True}}
    ]
    for i in range(len(data)):
        mock_user = User(username=unicode(i))
        mock_user.save()

        profile = GamecoachProfile(user=mock_user, roles=serialize_string_storage(data[i]['roles'], ROLES), regions=serialize_string_storage(data[i]['regions'], REGIONS_LABELS))
        profile.save()
        profiles.append(profile)
    return profiles


def serialize_string_storage(data_hash, value_list):
    if data_hash is None or data_hash == {}:
        return None
    return build_data_string(data_hash, value_list)


def build_data_string(data_hash, value_list):
    tokens = []
    for item in value_list:
        token = '0'
        if item in data_hash and data_hash[item] is True:
            token = '1'
        tokens.append(token)
    return '|'.join(tokens)
