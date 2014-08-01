
import os
from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from django_facebook.models import FacebookCustomUser as User

from profiles.tools.serialization import deserialize_roles, deserialize_regions, deserialize_availability, deserialize_data, deserialize_date


class GamecoachProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=128)
    roles = models.CharField(max_length=512, blank=True, null=True)
    regions = models.CharField(max_length=512, blank=True, null=True)
    availability = models.CharField(max_length=512, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created = models.DateField(default=datetime.now(), blank=True)
    updated = models.DateField(default=datetime.now(), blank=True)

    def deserialize(self):
        data = {
            'roles': deserialize_roles(self.roles),
            'regions': deserialize_regions(self.regions),
            'availability': deserialize_availability(self.availability),
            'data': deserialize_data(self.data),
            'created': deserialize_date(self.created),
            'updated': deserialize_date(self.updated)
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


class GamecoachProfileStudent(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=128)
    roles = models.CharField(max_length=512, blank=True, null=True)
    regions = models.CharField(max_length=512, blank=True, null=True)
    availability = models.CharField(max_length=512, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created = models.DateField(default=datetime.now(), blank=True)
    updated = models.DateField(default=datetime.now(), blank=True)

    def deserialize(self):
        data = {
            'roles': deserialize_roles(self.roles),
            'regions': deserialize_regions(self.regions),
            'availability': deserialize_availability(self.availability),
            'data': deserialize_data(self.data),
            'created': deserialize_date(self.created),
            'updated': deserialize_date(self.updated)
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
