from datetime import datetime

from django.db import models

from profiles.tools.serialization import deserialize_roles, deserialize_regions, deserialize_availability, deserialize_data, deserialize_date


class GamecoachProfile(models.Model):
    roles = models.CharField(max_length=512, blank=True, null=True)
    regions = models.CharField(max_length=512, blank=True, null=True)
    availability = models.CharField(max_length=512, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    created = models.DateField(default=datetime.now(), blank=True)
    updated = models.DateField(default=datetime.now(), blank=True)

    def deserialize(self):
        return {
            'roles': deserialize_roles(self.roles),
            'regions': deserialize_regions(self.regions),
            'availability': deserialize_availability(self.availability),
            'data': deserialize_data(self.data),
            'created': deserialize_date(self.created),
            'updated': deserialize_date(self.updated)
        }
