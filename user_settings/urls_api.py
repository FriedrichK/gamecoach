from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'logout', 'user_settings.views.logout', name='logout'),
    url(r'email', 'user_settings.views.email', name='email'),
    url(r'mentor_status', 'user_settings.views.mentor_status', name='mentor_status'),
)
