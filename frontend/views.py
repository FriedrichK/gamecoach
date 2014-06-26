from django.shortcuts import render
from django.http import Http404

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
