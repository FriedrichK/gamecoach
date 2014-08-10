
import os
from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from django_facebook.models import FacebookCustomUser as User
from django_facebook import signals
from django_facebook.utils import get_user_model
from django.contrib.auth.signals import user_logged_in

from profiles.tools.serialization import deserialize_roles, deserialize_regions, deserialize_mentoring, deserialize_availability, deserialize_data, deserialize_date


def activate_user(sender, user, request, **kwargs):
    if not user.is_active:
        user.is_active = True
        user.save()

user_logged_in.connect(activate_user, sender=get_user_model())


class GamecoachProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=128, unique=True)
    roles = models.CharField(max_length=512, blank=True, null=True)
    regions = models.CharField(max_length=512, blank=True, null=True)
    mentoring = models.CharField(max_length=512, blank=True, null=True)
    availability = models.CharField(max_length=512, blank=True, null=True)
    is_mentor = models.BooleanField(default=False)
    data = models.TextField(blank=True, null=True)
    created = models.DateField(default=datetime.now(), blank=True)
    updated = models.DateField(default=datetime.now(), blank=True)

    def deserialize(self):
        data = {
            'roles': deserialize_roles(self.roles),
            'regions': deserialize_regions(self.regions),
            'mentoring': deserialize_mentoring(self.mentoring),
            'availability': deserialize_availability(self.availability),
            'data': deserialize_data(self.data),
            'created': deserialize_date(self.created),
            'updated': deserialize_date(self.updated),
            'is_mentor': self.is_mentor
        }
        try:
            data['username'] = self.user.username
            data['name'] = self.username
            data['email'] = self.user.email
            data['first_name'] = self.user.first_name
            data['last_name'] = self.user.last_name
        except ObjectDoesNotExist:
            pass
        return data


def get_image_path(self, filename):
    return os.path.join(settings.MEDIA_ROOT, unicode(self.id), filename)


class ProfilePicture(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to=get_image_path)
    created = models.DateField(default=datetime.now(), blank=True)
