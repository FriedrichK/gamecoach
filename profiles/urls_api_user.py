from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'/(.*)', 'profiles.views_user.user', name='user'),
)
