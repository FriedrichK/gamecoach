#import os
import json
import urllib

from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def conversation(request, partnerId):
    if request.user is None or not request.user.is_authenticated():
        return HttpResponseForbidden(json.dumps({'success': False, 'message': 'access_not_allowed'}))
    if partnerId is None:
        return HttpResponseNotFound(json.dumps({'success': False, 'message': 'no_partner_id'}))
    return HttpResponse(json.dumps({}))


def conversation_retrieve(request, partner_id):
    pass


@csrf_exempt
def message(request, message_id):
    if request.method == "POST":
        if message_id is None or message_id == "None":
            return message_create(request)
        else:
            return message_update(request, message_id)
    if message_id is None:
        return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'missing_message_id'}))
    if request.method == "GET":
        return message_retrieve(request, message_id)
    if request.method == "DELETE":
        return message_delete(request, message_id)
    return HttpResponseBadRequest(json.dumps({'success': False, 'message': 'request_format_invalid'}))


def message_create(request):
    return HttpResponse('request')


def message_retrieve(request, message_id):
    return HttpResponse('retrieve')


def message_update(request, message_id):
    return HttpResponse('update')


def message_delete(request, message_id):
    return HttpResponse('delete')