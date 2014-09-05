import os
import unittest

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User

from shared.testing.factories.account import create_account
from gc_steam.tools import get_steam_id_from_uid, query_steam_api_to_get_player_summary, update_user_data_from_steam

MOCK_ENDPOINT = "http://this.is.not.a.real/openid"
MOCK_STEAM_ID = "12345"
MOCK_STEAM_PROFILE = {
    "steamid": "76561197960435530",
    "communityvisibilitystate": 3,
    "profilestate": 1,
    "personaname": "Robin",
    "lastlogoff": 1409845392,
    "profileurl": "http://steamcommunity.com/id/robinwalker/",
    "avatar": "http://media.steampowered.com/steamcommunity/public/images/avatars/f1/f1dd60a188883caf82d0cbfccfe6aba0af1732d4.jpg",
    "avatarmedium": "http://media.steampowered.com/steamcommunity/public/images/avatars/f1/f1dd60a188883caf82d0cbfccfe6aba0af1732d4_medium.jpg",
    "avatarfull": "http://media.steampowered.com/steamcommunity/public/images/avatars/f1/f1dd60a188883caf82d0cbfccfe6aba0af1732d4_full.jpg",
    "personastate": 0,
    "realname": "Robin Walker",
    "primaryclanid": "103582791429521412",
    "timecreated": 1063407589,
    "personastateflags": 0,
    "loccountrycode": "US",
    "locstatecode": "WA",
    "loccityid": 3961
}
MOCK_STEAM_USERNAME = "Robin"

SMOKE_TEST_SKIP_REASON = 'smoke tests are ignored ingored unless the environmental variable RUN_SMOKE_TESTS is set'


class ToolsSmokeTestCase(TestCase):

    @unittest.skipUnless('RUN_SMOKE_TESTS' in os.environ, SMOKE_TEST_SKIP_REASON)
    def test_returns_expected_user_profile(self):
        actual = query_steam_api_to_get_player_summary(settings.STEAM_TEST_UID)
        self.assertEquals(settings.STEAM_TEST_PERSONANAME, actual['personaname'])


class ToolsTestCase(TestCase):

    def test_returns_steam_id_from_steam_uid_uri(self):
        mock_steam_uid_uri = "%s/id/%s" % (MOCK_ENDPOINT, MOCK_STEAM_ID)

        actual = get_steam_id_from_uid(mock_steam_uid_uri, endpoint=MOCK_ENDPOINT)

        self.assertEquals(MOCK_STEAM_ID, actual)

    def test_updates_user_profile_with_steam_data_as_expected(self):
        account = create_account(provider='openid', user_values={'username': 'user', 'first_name': '', 'last_name': '', 'email': ''})
        user = account['user']

        # Delete Gamecoach profile, we do not have it at this point
        user.gamecoachprofile.delete()
        user = User.objects.get(id=user.id)

        user = update_user_data_from_steam(user, MOCK_STEAM_PROFILE)
        user = User.objects.get(id=user.id)

        self.assertEquals(user.username, MOCK_STEAM_USERNAME)
        self.assertEquals(user.gamecoachprofile.username, MOCK_STEAM_USERNAME)

    def test_modifies_username_for_main_user_table_if_given_username_is_taken(self):
        account = create_account(provider='openid', user_values={'username': 'Robin', 'first_name': '', 'last_name': '', 'email': ''})
        account = create_account(provider='openid', user_values={'username': 'user', 'first_name': '', 'last_name': '', 'email': ''})
        user = account['user']

        # Delete Gamecoach profile, we do not have it at this point
        user.gamecoachprofile.delete()
        user = User.objects.get(id=user.id)

        user = update_user_data_from_steam(user, MOCK_STEAM_PROFILE)
        user = User.objects.get(id=user.id)

        self.assertEquals(user.username, "%s1" % MOCK_STEAM_USERNAME)
        self.assertEquals(user.gamecoachprofile.username, "%s1" % MOCK_STEAM_USERNAME)
