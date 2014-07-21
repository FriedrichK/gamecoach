from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'/(.*)/profilePicture', 'profiles.views.profile_picture', name='profile_picture'),
)
