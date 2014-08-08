import json


def get_email(user):
    if not user or not hasattr(user, 'gamecoachprofile') or user.gamecoachprofile is None:
        return None

    data = json.loads(user.gamecoachprofile.data)
    if not 'email' in data:
        return None
    return data['email']
