from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'', 'profiles.views.mentor', {'mentor_id': None}, name='mentor'),
)
