from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', 'frontend.views.index', name='index'),
)
