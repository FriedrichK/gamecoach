# Adpated from: http://andrefsp.wordpress.com/2012/05/31/unit-testing-django-south-migrations/

from django.test import TestCase
from django.db import models
from django.core.management import call_command
from django.db.models import loading
loading.cache.loaded = False

from django.contrib.sites.models import Site

from south.migration import Migrations


class TestOrm:
    def __init__(self):
        setattr(self, 'sites.site', Site)


class MyMigrationTest(TestCase):

    def setUp(self):
        Model = FacebookCustomUser
        call_command('syncdb', verbosity=0, interactive=False)

    def _pick_migration(self, app_label, migration_name):
        migrations = Migrations(app_label)
        for migration in migrations:
            if migration.full_name().split('.')[-1] == migration_name:
                return migration
        return None

    def test_0002_migrate_existing_accounts_from_django_facebook_to_django_allauth(self):
        self.migration = self._pick_migration('shared', '0002_migrate_existing_accounts_from_django_facebook_to_django_allauth')
        if not self.migration:
            return

        orm = TestOrm()
        self.migration.migration_instance().forwards(orm)

        self.assertEquals(True, False)


class FacebookCustomUser(models.Model):
    about_me = models.TextField(blank=True, null=True)
    facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
    access_token = models.TextField(blank=True, help_text='Facebook token for offline access', null=True)
    facebook_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_profile_url = models.TextField(blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    blog_url = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
