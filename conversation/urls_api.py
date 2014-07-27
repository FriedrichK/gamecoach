from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'/message/(.*)', 'conversation.views.message', name='message'),
    url(r'/(.*)', 'conversation.views.conversation', name='conversation'),
)
