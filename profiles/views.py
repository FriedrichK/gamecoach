import json
import urllib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tools.mentors import get_all_mentors


@csrf_exempt
def mentor(request, mentor_id):
    role = request.GET.get('role', None)
    print "role is", role
    if role is not None:
        role = urllib.unquote(role)
        print "before JSON load", role
        print json.loads(role)
    return HttpResponse(json.dumps(get_all_mentors()))
