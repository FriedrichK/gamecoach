import json
import urllib

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from tools.mentors import get_all_mentors


@csrf_exempt
def mentor(request, mentor_id):
    filters = {}
    filter_categories = ['roles', 'regions', 'availability']
    for filter_category in filter_categories:
        raw_filter = request.GET.get(filter_category, None)
        if not raw_filter is None:
            filters[filter_category] = json.loads(urllib.unquote(raw_filter))
    return HttpResponse(json.dumps(get_all_mentors(filters)))
