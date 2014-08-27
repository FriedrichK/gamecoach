from south.v2 import DataMigration
from django.conf import settings


class Migration(DataMigration):
    def forwards(self, orm):
        site = self._forward_ensure_primary_site_is_set_up_correctly(orm)
        self._forward_ensure_facebook_provider_exists(orm, site)

    def _forward_ensure_primary_site_is_set_up_correctly(self, orm):
        Site = orm['sites.Site']
        site, created = Site.objects.get_or_create(id=settings.SITE_ID)
        site.domain = settings.SITE_DOMAIN
        site.name = settings.SITE_NAME
        site.save()
        return site

    def _forward_ensure_facebook_provider_exists(self, orm, site):
        SocialApp = orm['socialaccount.SocialApp']
        provider, created = SocialApp.objects.get_or_create(provider='facebook', name='Facebook')
        provider.secret = settings.FACEBOOK_APP_SECRET
        provider.client_id = settings.FACEBOOK_APP_ID
        provider.key = ''
        provider.sites.add(site)
        provider.save()
        return provider

    def backwards(self, orm):
        pass

    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'socialaccount.socialapp': {
            'Meta': {'object_name': 'SocialApp'},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['shared']
