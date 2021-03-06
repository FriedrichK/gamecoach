from django.conf.urls import patterns, include, url, handler404, handler500

from django.contrib import admin
admin.autodiscover()

from frontend.views import page404, page500

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),

    url(r'files/(.*)', 'profiles.views.profile_picture', 'p'),

    (r'^accounts/', include('allauth.urls')),

    url(r'^api/mentor', include('profiles.urls_api')),
    url(r'^data/mentor', include('profiles.urls_data')),

    url(r'^api/settings', include('user_settings.urls_api')),

    url(r'^api/conversation', include('conversation.urls_api')),

    url(r'^', include('frontend.urls')),
)

handler404 = page404
handler500 = page500
