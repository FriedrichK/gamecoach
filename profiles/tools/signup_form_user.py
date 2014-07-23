from profiles.tools.signup_form import generate_form_data


def add_profile_for_user(Model, user, form):
    profile = build_profile_from_signup_form_data(Model, form)
    setattr(profile, 'user', user)
    return profile.save()


def update_profile_for_user(model_identifier, user, form):
    profile = getattr(user, model_identifier)
    model_data = generate_form_data(form)
    for label, value in model_data.items():
        setattr(profile, label, value)
    return profile.save()


def build_profile_from_signup_form_data(Model, signup_form_data):
    model_data = generate_form_data(signup_form_data)
    return Model(**model_data)
