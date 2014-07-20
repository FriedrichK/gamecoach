from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'/profilePicture/(.*)', 'profiles.views.profile_picture', name='profile_picture'),
    url(r'/(.*)', 'profiles.views.mentor', name='mentor'),
    url(r'', 'profiles.views.mentor', {'mentor_id': None}, name='mentor'),
)
