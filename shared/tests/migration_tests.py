# Adpated from: http://andrefsp.wordpress.com/2012/05/31/unit-testing-django-south-migrations/

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.management import call_command
from django.db.models import loading
loading.cache.loaded = False

from django.contrib.sites.models import Site

from south.migration import Migrations

MODIFIED_INSTALLED_APPS = tuple(list(settings.INSTALLED_APPS) + ['shared.tests'])


class TestOrm:
    def __init__(self):
        setattr(self, 'sites.site', Site)


class MyMigrationTest(TestCase):

    new_settings = dict(
        INSTALLED_APPS=MODIFIED_INSTALLED_APPS
    )

    _override = None

    def setUp(self):
        self._override = override_settings(**self.new_settings)
        self._override.enable()
        call_command('syncdb', verbosity=2, interactive=False)

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
