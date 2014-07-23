import urllib
import json

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from profiles.tools.profile_methods import get_profile_by_id, get_all_profiles
from profiles.tools.signup_form import get_mentor_signup_form_from_request
from profiles.tools.signup_form_user import add_profile_for_user, update_profile_for_user

from profiles.models import GamecoachProfileStudent


@csrf_exempt
def user(request, user_id):
    if request.method == "POST":
        return user_create_or_update(request, user_id)
    if request.method == "GET":
        return user_read(request, user_id)


def user_read(request, mentor_id):
    if mentor_id is None:
        return get_filtered_users(request)
    else:
        mentor = get_profile_by_id(GamecoachProfileStudent, mentor_id)
        if mentor is None:
            return HttpResponseNotFound()
        return HttpResponse(json.dumps(mentor.deserialize()))


def user_create_or_update(request, user_id):
    user_signup_form = get_mentor_signup_form_from_request(json.loads(request.body))
    if request.user is None or not request.user.is_authenticated():
        return HttpResponseNotFound(json.dumps({'success': False, 'error': 'no_valid_user_found'}))
    if not hasattr(request.user, 'gamecoachprofilestudent'):
        return user_create(request, user_signup_form)
    return user_update(request, user_id, user_signup_form)


def user_create(request, user_signup_form):
    result = add_profile_for_user(GamecoachProfileStudent, request.user, user_signup_form)
    return HttpResponse(json.dumps({'bla': 'bla'}))


def user_update(request, user_id, user_signup_form):
    result = update_profile_for_user('gamecoachprofilestudent', request.user, user_signup_form)
    return HttpResponse(json.dumps({'bla': 'blub'}))


def get_filtered_users(request):
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
    return HttpResponse(json.dumps(get_all_profiles(GamecoachProfileStudent, filters)))
