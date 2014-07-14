from profiles.settings import SIGNUP_FORM


def add_profile_for_user(user, form):
    pass


def get_mentor_signup_form_from_request(data):
    form_content = {}
    for key, value in SIGNUP_FORM.items():
        item = None
        if key in data:
            item = data[key]
        form_content[key] = item
    return form_content
