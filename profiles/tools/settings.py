def get_email(user):
    if not user or not hasattr(user, 'gamecoachprofile') or user.gamecoachprofile is None:
        return None

    return user.gamecoachprofile.email
