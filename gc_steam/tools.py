import json

from django.conf import settings
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User

import requests

from profiles.models import GamecoachProfile

PLACEHOLDER_USERNAME_FOR_OPENID_ACCOUNTS_WE_CANNOT_LEAVE_UNMODIFIED = "user"


def get_steam_id_from_uid(uid, endpoint=settings.STEAM_OPENID_ENDPOINT):
    prefix = "%s/id/" % endpoint
    return uid.replace(prefix, '')


def query_steam_api_to_get_player_summary(
    steam_id, api_key=settings.STEAM_API_KEY,
    api_root=settings.STEAM_API_ROOT,
    api_endpoint='/ISteamUser/GetPlayerSummaries/v0002/',
    format='json'
):
    result_for_multiple_players = query_steam_api_to_get_player_summaries(
        [steam_id],
        api_key=api_key,
        api_root=api_root,
        api_endpoint=api_endpoint,
        format=format
    )
    if result_for_multiple_players is None or len(result_for_multiple_players) < 1:
        return None
    return result_for_multiple_players[0]


def query_steam_api_to_get_player_summaries(
    steam_ids, api_key=settings.STEAM_API_KEY,
    api_root=settings.STEAM_API_ROOT,
    api_endpoint='/ISteamUser/GetPlayerSummaries/v0002/',
    format='json'
):
    uri = '%s%s' % (api_root, api_endpoint)
    payload = {
        'key': api_key,
        'steamids': ','.join([unicode(steam_id) for steam_id in steam_ids]),
        'format': format
    }
    result, status_code = query_steam_api(uri, payload)
    if result is None or not 'response' in result or not 'players' in result['response'] or len(result['response']['players']) < 1:
        return None
    return result['response']['players']


def query_steam_api(uri, params, format='json'):
    r = requests.get(uri, params=dict(params.items() + {'format': format}.items()))
    if r.status_code == 500:
        raise SteamApiInternalError()
    if r.status_code == 404:
        raise SteamApiNotFoundError()
    if not r.status_code == requests.codes.ok:
        raise SteamApiError(json.dumps({'status_code': r.status_code, 'message': r.text}))
    return json.loads(r.text), r.status_code


class SteamApiError(Exception):
    pass


class SteamApiInternalError(SteamApiError):
    pass


class SteamApiNotFoundError(SteamApiError):
    pass


def update_user_data_from_steam(user, steam_data):
    user = update_main_user_entry_from_steam(user, steam_data)
    user = update_gamecoach_profile_from_steam(user, steam_data)
    return user


def update_main_user_entry_from_steam(user, steam_data):
    if user.username == PLACEHOLDER_USERNAME_FOR_OPENID_ACCOUNTS_WE_CANNOT_LEAVE_UNMODIFIED:
        try:
            user.username = steam_data["personaname"]
            with transaction.atomic():
                user.save()
        except IntegrityError:
            users = User.objects.filter(username__startswith=user.username)
            usernames = [u.username for u in users]

            username = user.username
            index = 1
            while username in usernames:
                username = user.username + unicode(index)
                index += 1

            user.username = username
            user.save()
    return user


def update_gamecoach_profile_from_steam(user, steam_data):
    if hasattr(user, 'gamecoachprofile'):
        profile = user.gamecoachprofile
    else:
        profile = GamecoachProfile(user=user)
    try:
        with transaction.atomic():
            profile.username = user.username
            profile.save()
    except IntegrityError:
        profiles = GamecoachProfile.objects.filter(username__startswith=user.username)
        usernames = [p.username for p in profiles]
        viable_username = get_viable_username(user.username, usernames)
        profile.username = viable_username
        profile.save()
    return user


def get_viable_username(username, taken_usernames):
    index = 1
    uname = username
    while uname in taken_usernames:
        uname = username + unicode(index)
        index += 1
    return uname
