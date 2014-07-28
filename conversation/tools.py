def is_allowed_to_read_all_messages(user):
    if user.is_superuser or user.is_staff:
        return True
    return False
