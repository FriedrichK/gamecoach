#import os
import json
import urllib

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from profiles.tools.mentors import get_all_mentors, get_mentor_by_id, get_mentor_by_username
from profiles.tools.profile_methods import get_profile_by_username
from profiles.tools.signup_form import add_profile_for_user, update_profile_for_user, get_mentor_signup_form_from_request
from profiles.models import ProfilePicture


@csrf_exempt
def mentor(request, mentor_id):
    if request.method == "POST":
        return mentor_create_or_update(request, mentor_id)
    if request.method == "GET":
        return mentor_read(request, mentor_id)
    if request.method == "DELETE":
        return mentor_delete(request, mentor_id)


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
    if not hasattr(request.user, 'gamecoachprofile'):
        return mentor_create(request, mentor_signup_form)
    return mentor_update(request, mentor_id, mentor_signup_form)


def mentor_create(request, mentor_signup_form):
    result = add_profile_for_user(request.user, mentor_signup_form)
    return HttpResponse(json.dumps({'successs': True}))


def mentor_update(request, mentor_id, mentor_signup_form):
    result = update_profile_for_user(request.user, mentor_signup_form)
    return HttpResponse(json.dumps({'success': True}))


def mentor_delete(request, mentor_id):
    if request.user is None or not request.user.is_authenticated():
        return HttpResponseNotFound(json.dumps({'success': False, 'error': 'no_valid_user_found'}))
    if not request.user.username == mentor_id:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'access denied'}))
    request.user.is_active = False
    request.user.save()

    return HttpResponse(json.dumps({'success': True, 'message': 'user deactivated'}))


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


@csrf_exempt
def profile_picture(request, user_id):
    if request.method == "GET":
        return profile_picture_display(request, user_id)
    if request.method == "POST":
        return profile_picture_upload(request)


@csrf_exempt
def profile_username(request):
    username = request.GET.get('value', None)

    no_username_message = json.dumps({'success': False, 'message': 'username %s does not exist' % username})
    username_message = json.dumps({'success': True, 'message': 'username %s exists' % username})

    if not username is None and not username == '' and not get_profile_by_username(username) is None:
        return HttpResponse(username_message)
    return HttpResponseNotFound(no_username_message)


def profile_picture_display(request, username):
    try:
        user = get_mentor_by_username(username)
        picture = ProfilePicture.objects.get(user=user)
        image_path = unicode(picture.image)
        image_path = image_path.replace(settings.MEDIA_ROOT, '')
        final_path = '/upload' + image_path
        response = HttpResponse()
        del response['content-type']
        response['X-Accel-Redirect'] = final_path
        return response
    except ProfilePicture.DoesNotExist:
        return HttpResponseNotFound()
    return HttpResponse(json.dumps({}))


def profile_picture_upload(request):
    for f in request.FILES.getlist('file'):
        profile_picture, created = ProfilePicture.objects.get_or_create(user=request.user)
        profile_picture.image = f
        profile_picture.save()
    return HttpResponse(json.dumps({}))
