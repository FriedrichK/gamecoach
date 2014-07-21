from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    #url(r'files/(.*)', 'profiles.views.profile_picture', 'p'),

    url(r'^facebook/', include('django_facebook.urls')),
    url(r'^accounts/', include('django_facebook.auth_urls')),

    url(r'^api/mentor', include('profiles.urls_api')),
    url(r'^data/mentor', include('profiles.urls_data')),
    url(r'^api/message', include('privatemessages.urls_api')),
    url(r'^', include('frontend.urls')),
)
