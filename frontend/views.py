from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from profiles.tools.mentors import get_mentor_by_id


def index(request):
    context = get_basic_context(request)
    return render(request, 'pages/index/index.html', context)


def login(request):
    context = get_basic_context(request)
    data = {
        'facebook_app_id': settings.FACEBOOK_APP_ID
    }
    return render(request, 'pages/user_login/user_login.html', dict(context.items() + data.items()))


def results(request):
    context = get_basic_context(request)
    return render(request, 'pages/mentor_results/mentor_results.html', context)


def mentor(request, mentor_id):
    mentor = get_mentor_by_id(mentor_id)
    if mentor is None:
        raise Http404()

    context = {
        'mentor_id': mentor_id
    }
    context = dict(context.items() + get_basic_context(request).items())
    return render(request, 'pages/mentor_profile/mentor_profile.html', context)


def register_mentor(request):
    context = get_basic_context(request)
    if not request.user.is_authenticated():
        data = {
            'facebook_app_id': settings.FACEBOOK_APP_ID
        }
        return render(request, 'pages/mentor_signup/mentor_signup_step1.html', dict(context.items() + data.items()))
    else:
        return render(request, 'pages/mentor_signup/mentor_signup_step2.html', context)


def mentor_contact(request, user_id):
    context = get_basic_context(request)
    if not request.user.is_authenticated():
        data = {
            'user_id': user_id,
            'facebook_app_id': settings.FACEBOOK_APP_ID
        }
        return render(request, 'pages/mentor_contact/mentor_contact_step1.html', dict(context.items() + data.items()))
    if not is_user(request.user):
        return render(request, 'pages/mentor_contact/mentor_contact_step2.html', context)
    return render(request, 'pages/conversation/inbox.html', context)


def get_basic_context(request):
    return {
        'is_mentor': is_mentor(request.user),
        'is_authenticated': request.user.is_authenticated(),
        'username': request.user.username
    }


def is_mentor(user):
    return has_profile(user, 'gamecoachprofile')


def is_user(user):
    return has_profile(user, 'gamecoachprofilestudent')


def has_profile(user, profile_name):
    if not hasattr(user, 'gamecoachprofile') or user.gamecoachprofile is None:
        return False
    return True
