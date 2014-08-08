def user_is_available(user):
    if not user.is_authenticated or not user.is_active:
        return False
    return True
