import json

from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from shared.tools import check_request_requirements
from privatemessages.tools import get_recipients, create_message


@csrf_exempt
def message(request, message_id):
    if message_id is None:
        return request_without_id(request)
    else:
        return request_with_id(request, message_id)


def request_without_id(request):
    if request.method == "POST":
        return view_create_message(request)
    else:
        return view_read_messages(request)


def request_with_id(request, message_id):
    if request.method == "POST":
        return view_update_message(request, message_id)
    if request.method == "DELETE":
        return view_delete_message(request, message_id)
    return view_read_message(request, message_id)


def view_create_message(request):
    requirements = []
    if not check_request_requirements(request, 'POST', requirements):
        return HttpResponseBadRequest

    options = {
        'sender': None,
        'subject': request.POST.get('body'),
        'body': request.POST.get('body')
    }
    recipient_list_raw = request.POST.get('recipients', '[]')
    recipient_list = json.loads(recipient_list_raw)
    recipients = get_recipients(recipient_list)

    result = create_message(recipients, options)
    return HttpResponse(json.dumps(result))


def view_read_messages(request):
    data = {'test': True}
    return HttpResponse(json.dumps(data))


def view_read_message(request):
    data = {'test': True}
    return HttpResponse(json.dumps(data))


def view_update_message(request):
    data = {'test': True}
    return HttpResponse(json.dumps(data))


def view_delete_message(request):
    data = {'test': True}
    return HttpResponse(json.dumps(data))
