from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'login', 'frontend.views.login', name='login'),
    url(r'settings', 'frontend.views.edit_settings', name='settings'),
    url(r'inbox', 'frontend.views.message_hub', name='message_hub'),
    url(r'results', 'frontend.views.results', name='results'),
    url(r'profile/edit', 'frontend.views.edit_profile', name='edit_profile'),
    url(r'mentor/(.*)/contact', 'frontend.views.mentor_contact', name='mentor_contact'),
    url(r'mentor/(.*)', 'frontend.views.mentor', name='mentor'),
    url(r'register/mentor', 'frontend.views.register_mentor', name='register_mentor'),
    url(r'conversation/(.*)', 'frontend.views.conversation', name='conversation'),
    url(r'', 'frontend.views.index', name='index'),
)
