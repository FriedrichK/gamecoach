from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^api/mentor', include('profiles.urls_api')),
    url(r'^api/message', include('privatemessages.urls_api')),
    url(r'^', include('frontend.urls')),
)
