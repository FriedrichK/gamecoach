from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'/(.*)', 'privatemessages.views.message', name='message'),
    url(r'', 'privatemessages.views.message', {'message_id': None}, name='message'),
)
