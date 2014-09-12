from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'/profilePicture/(.*)', 'profiles.views.profile_picture', name='profile_picture'),
    url(r'/profileUsername/', 'profiles.views.profile_username', name='profile_username'),
    url(r'/(.*)', 'profiles.views.mentor', name='mentor'),
    url(r'/?', 'profiles.views.mentor', {'mentor_id': None}, name='mentor'),
)
