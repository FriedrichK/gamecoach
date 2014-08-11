import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from profiles.tools.auth import user_is_available


@csrf_exempt
def email(request):
    if not user_is_ok(request.user) is True:
        return user_is_ok(request.user)

    try:
        request_data = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'request is not valid JSON'}))

    if not 'email' in request_data or not 'email2' in request_data:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'request needs to contain both an email (email) and the email confirmation (email2)'}))

    if not request_data['email'] == request_data['email2']:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'email and confirmation do not match'}))

    request.user.gamecoachprofile.email = request_data['email']
    request.user.gamecoachprofile.save()

    return HttpResponse(json.dumps({'success': True, 'message': 'email changed to %s' % (request_data['email'])}))


@csrf_exempt
def mentor_status(request):
    if not user_is_ok(request.user) is True:
        return user_is_ok(request.user)

    request_data = request_contains(request.body, ['status'])
    if isinstance(request_data, HttpResponseBadRequest):
        return request_data
    if not isinstance(request_data, dict):
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'invalid format for request data'}))
    if not isinstance(request_data['status'], bool):
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'status has to be a boolean value'}))

    request.user.gamecoachprofile.is_mentor = request_data['status']
    request.user.gamecoachprofile.save()

    return HttpResponse(json.dumps({'success': True, 'message': 'mentor status changed to %s' % request_data['status']}))


def user_is_ok(user):
    if not user_is_available(user):
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'no_valid_user_found'}))
    if not hasattr(user, 'gamecoachprofile') or user.gamecoachprofile is None:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'user does not have a profile yet'}))
    return True


def request_contains(request_body, parameters):
    try:
        request_data = json.loads(request_body)
    except ValueError:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'request is not valid JSON'}))

    missing = []
    for parameter in parameters:
        if not parameter in request_data:
            missing.append(parameter)

    if len(missing) == 0:
        return request_data

    if len(missing) == 1:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'request is missing parameter: %s' % missing[0]}))

    if len(missing) > 1:
        return HttpResponseBadRequest(json.dumps({'success': False, 'error': 'request is missing parameters: %s' % (', '.join(missing))}))
