from django.shortcuts import render


def index(request):
    return render(request, 'pages/index/index.html')


def results(request):
    return render(request, 'pages/mentor_results/mentor_results.html')


def mentor(request, mentor_id):
    data = {
        'mentor_id': mentor_id
    }
    return render(request, 'pages/mentor_profile/mentor_profile.html', data)
