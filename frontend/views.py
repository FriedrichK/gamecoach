import json
from operator import itemgetter

from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.conf import settings

from django_facebook.models import FacebookCustomUser as User

from profiles.tools.mentors import get_mentor_by_id, get_mentor_by_username
from profiles.settings import HEROES_HASH


def index(request):
    context = get_basic_context(request)
    if request.user.is_authenticated and request.user.is_active:
        return render(request, 'pages/conversation/hub.html', context)
    else:
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

    if not has_profile(request.user):
        return render(request, 'pages/mentor_signup/mentor_signup_step2.html', context)

    return render(request, 'pages/conversation/hub.html', context)


def mentor_contact(request, user_id):
    context = get_basic_context(request)
    data = {
        'user_id': user_id,
        'facebook_app_id': settings.FACEBOOK_APP_ID
    }
    if not request.user.is_authenticated():
        return render(request, 'pages/mentor_contact/mentor_contact_step1.html', dict(context.items() + data.items()))

    if request.user.username == user_id:
        return render(request, 'pages/conversation/hub.html', context)

    if not has_profile(request.user):
        return render(request, 'pages/mentor_contact/mentor_contact_step2.html', dict(context.items() + data.items()))

    if get_mentor_by_username(user_id) is None:
        raise Http404()

    return render(request, 'pages/conversation/inbox.html', dict(context.items() + data.items()))


def conversation(request, user_id):
    context = get_basic_context(request)
    data = {
        'user_id': user_id,
    }

    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login?next=/conversation/' + user_id)

    if request.user.username == user_id:
        return render(request, 'pages/conversation/hub.html', context)

    return render(request, 'pages/conversation/inbox.html', dict(context.items() + data.items()))


def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    profile = {}
    if has_profile(request.user):
        profile = request.user.gamecoachprofile.deserialize()
    if 'data' in profile and 'top_heroes' in profile['data']:
        profile['data']['top_heroes'] = post_process_top_heroes(profile['data']['top_heroes'])
    print profile

    context = get_basic_context(request)
    context['profile'] = profile
    context['user_id'] = request.user.username
    context['top_heroes'] = build_top_heroes_list(HEROES_HASH)
    return render(request, 'pages/account/profile.html', context)


def get_basic_context(request):
    return {
        'is_mentor': has_profile(request.user),
        'is_authenticated': request.user.is_authenticated(),
        'username': get_username(request.user)
    }


def has_profile(user):
    if not hasattr(user, 'gamecoachprofile') or user.gamecoachprofile is None:
        return False
    return True


def get_username(user):
    if has_profile(user):
        if not user.gamecoachprofile.data is None:
            data = json.loads(user.gamecoachprofile.data)
            if 'steamId' in data:
                return data['steamId']
    return user.username


def post_process_top_heroes(raw_top_heroes):
    top_heroes = []
    for label in raw_top_heroes:
        for key, value in HEROES_HASH.items():
            if value == label:
                top_heroes.append((key, value,))
    return top_heroes


def build_top_heroes_list(hash):
    top_heroes_list = []
    for key, value in hash.items():
        top_heroes_list.append((key, value,))
    top_heroes_list = sorted(top_heroes_list, key=itemgetter(1))
    return top_heroes_list
