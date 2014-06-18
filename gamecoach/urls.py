from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'results', 'frontend.views.results', name='results'),
    url(r'', 'frontend.views.index', name='index'),
)
