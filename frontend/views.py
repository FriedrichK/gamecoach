from django.shortcuts import render


def index(request):
    return render(request, 'pages/index/index.html')


def results(request):
    return render(request, 'pages/mentor_results/mentor_results.html')
