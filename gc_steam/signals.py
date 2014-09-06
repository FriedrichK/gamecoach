from allauth.account.signals import user_logged_in

from gc_steam.tools import get_steam_id_from_uid, query_steam_api_to_get_player_summary, update_user_data_from_steam, SteamApiError


def on_steam_user_logged_in(sender, user, request, **kwargs):
    if not hasattr(user, 'socialaccount_set'):
        return

    socialaccounts = user.socialaccount_set.all()
    open_id_provider = get_open_id_provider(socialaccounts)
    if open_id_provider is None:
        return

    steam_id = get_steam_id_from_uid(open_id_provider.uid)
    if steam_id is None:
        return

    try:
        profile = query_steam_api_to_get_player_summary(steam_id)
    except SteamApiError:
        profile = {'personaname': 'user1'}

    update_user_data_from_steam(request.user, profile)


def get_open_id_provider(socialaccounts):
    for socialaccount in socialaccounts:
        if socialaccount.provider == "openid":
            return socialaccount
    return None


user_logged_in.connect(on_steam_user_logged_in)
