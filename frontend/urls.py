from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'results', 'frontend.views.results', name='results'),
    url(r'mentor/(.*)/contact', 'frontend.views.mentor_contact', name='mentor_contact'),
    url(r'mentor/(.*)', 'frontend.views.mentor', name='mentor'),
    url(r'register/mentor', 'frontend.views.register_mentor', name='register_mentor'),
    url(r'', 'frontend.views.index', name='index'),
)
