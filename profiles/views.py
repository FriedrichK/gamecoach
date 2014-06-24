import json
import urllib

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from tools.mentors import get_all_mentors, get_mentor_by_id


@csrf_exempt
def mentor(request, mentor_id):
    if mentor_id is None:
        return get_filtered_mentors(request)
    else:
        mentor = get_mentor_by_id(mentor_id)
        if mentor is None:
            return HttpResponseNotFound()
        return HttpResponse(json.dumps(mentor.deserialize()))


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
