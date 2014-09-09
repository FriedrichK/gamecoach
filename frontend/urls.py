from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^about/?$', 'frontend.views.about', name='about'),
    url(r'^contact/?$', 'frontend.views.contact', name='contact'),
    url(r'^cookies/?$', 'frontend.views.cookies', name='cookies'),
    url(r'^privacy/?$', 'frontend.views.privacy', name='privacy'),
    url(r'^suggestions/?$', 'frontend.views.suggestions', name='suggestions'),
    url(r'^terms/?$', 'frontend.views.terms', name='terms'),

    url(r'^login/redirect/', 'frontend.views.login_redirect', name='login_redirect'),
    url(r'^login', 'frontend.views.login', name='login'),
    url(r'^settings', 'frontend.views.edit_settings', name='settings'),
    url(r'^inbox', 'frontend.views.message_hub', name='message_hub'),
    url(r'^results', 'frontend.views.results', name='results'),
    url(r'^profile/$', 'frontend.views.profile', name='profile'),
    url(r'^profile/edit', 'frontend.views.edit_profile', name='edit_profile'),
    url(r'^mentor/(.*)/contact', 'frontend.views.mentor_contact', name='mentor_contact'),
    url(r'^mentor/(.*)', 'frontend.views.mentor', name='mentor'),
    url(r'^register/mentor/?', 'frontend.views.register_mentor', name='register_mentor'),
    url(r'^register/student/?', 'frontend.views.register_student', name='register_student'),
    url(r'^conversation/(.*)', 'frontend.views.conversation', name='conversation'),
    url(r'', 'frontend.views.index', name='index'),
)
