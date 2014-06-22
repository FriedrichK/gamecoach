from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'results', 'frontend.views.results', name='results'),

    url(r'^api/mentor', include('profiles.urls_api')),

    url(r'', 'frontend.views.index', name='index'),
)
