import json
import urllib

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from tools.mentors import get_all_mentors, get_mentor_by_id
from tools.signup_form import add_profile_for_user, update_profile_for_user, get_mentor_signup_form_from_request


@csrf_exempt
def mentor(request, mentor_id):
    if request.method == "POST":
        return mentor_create_or_update(request, mentor_id)
    if request.method == "GET":
        return mentor_read(request, mentor_id)


def mentor_read(request, mentor_id):
    if mentor_id is None:
        return get_filtered_mentors(request)
    else:
        mentor = get_mentor_by_id(mentor_id)
        if mentor is None:
            return HttpResponseNotFound()
        return HttpResponse(json.dumps(mentor.deserialize()))


def mentor_create_or_update(request, mentor_id):
    mentor_signup_form = get_mentor_signup_form_from_request(json.loads(request.body))
    if request.user is None or not request.user.is_authenticated():
        return HttpResponseNotFound(json.dumps({'success': False, 'error': 'no_valid_user_found'}))
    if request.user.gamecoachprofile is None:
        return mentor_create(request, mentor_signup_form)
    return mentor_update(request, mentor_id, mentor_signup_form)


def mentor_create(request, mentor_signup_form):
    result = add_profile_for_user(request.user, mentor_signup_form)
    return HttpResponse(json.dumps({'bla': 'bla'}))


def mentor_update(request, mentor_id, mentor_signup_form):
    result = update_profile_for_user(request.user, mentor_signup_form)
    return HttpResponse(json.dumps({'bla': 'blub'}))


def get_filtered_mentors(request):
    filters = {}
    filter_categories = ['roles', 'regions', 'day', 'time']
    for filter_category in filter_categories:
        raw_filter = request.GET.get(filter_category, None)
        if not raw_filter is None:
            if filter_category == "day" or filter_category == "time":
                filter_value = {}
                filter_value[raw_filter] = True
            else:
                filter_value = json.loads(urllib.unquote(raw_filter))
            filters[filter_category] = filter_value
    return HttpResponse(json.dumps(get_all_mentors(filters)))
