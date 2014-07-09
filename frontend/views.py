from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from profiles.tools.mentors import get_mentor_by_id


def index(request):
    return render(request, 'pages/index/index.html')


def results(request):
    return render(request, 'pages/mentor_results/mentor_results.html')


def mentor(request, mentor_id):
    mentor = get_mentor_by_id(mentor_id)
    if mentor is None:
        raise Http404()

    data = {
        'mentor_id': mentor_id
    }
    return render(request, 'pages/mentor_profile/mentor_profile.html', data)


def register_mentor(request):
    if not request.user.is_authenticated():
        data = {
            'facebook_app_id': settings.FACEBOOK_APP_ID
        }
        return render(request, 'pages/mentor_signup/mentor_signup_step1.html', data)
    else:
        return render(request, 'pages/mentor_signup/mentor_signup_step2.html')
