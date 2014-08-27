#import os
import json

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from django.contrib.auth.models import User

from profiles.tools.mentors import get_mentor_by_username
from conversation.tools_message import create_message, serialize_message
from conversation.tools_folder import get_conversation, get_inbox_slice


@csrf_exempt
def conversation(request, partner_id):
    if request.user is None or not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseForbidden(json.dumps({'success': False, 'message': 'access_not_allowed'}))

    if partner_id is None or partner_id == "":
        message_items = get_inbox_slice(request.user, now(), items=500)
        messages = [serialize_message(message) for message in message_items]
        return HttpResponse(json.dumps(messages))

    conversation_partner = get_mentor_by_username(partner_id)
    if conversation_partner is None or not conversation_partner.is_active:
        return HttpResponseNotFound(json.dumps({'success': False, 'message': 'other user in the conversation could not be found'}))

    conversation = get_conversation(request.user, [conversation_partner])
    messages = [serialize_message(message) for message in conversation]

    return HttpResponse(json.dumps(messages))


def conversation_retrieve(request, partner_id):
    pass


@csrf_exempt
def message(request, message_id):
    if request.method == "POST":
        if message_id is None or message_id == "None" or message_id == "":
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
    if request.user is None or not request.user.is_authenticated() or not request.user.is_active:
        return HttpResponseForbidden(json.dumps({'success': False, 'message': 'access_not_allowed'}))

    data = json.loads(request.body)

    if not 'message' in data or data['message'] is None or data['message'] == "":
        return HttpResponseForbidden(json.dumps({'success': False, 'message': 'you have not provided a message body or the message body is empty'}))

    recipient_user = get_recipient_from_data(data)
    if recipient_user is None or not recipient_user.is_active:
        return HttpResponseNotFound(json.dumps({'success': False, 'message': 'recipient user could not be found or is inactive'}))

    if recipient_user == request.user:
        return HttpResponseForbidden(json.dumps({'success': False, 'message': 'recipient is you. You cannot send yourself a message'}))

    message = create_message(request.user, recipient_user, '[automatic]', data['message'])

    return HttpResponse('create')


def message_retrieve(request, message_id):
    return HttpResponse('retrieve')


def message_update(request, message_id):
    return HttpResponse('update')


def message_delete(request, message_id):
    return HttpResponse('delete')


def get_recipient_from_data(data):
    if data is None or not 'recipient' in data:
        return None
    try:
        user = User.objects.get(username=data['recipient'])
        return user
    except User.DoesNotExist:
        return None
