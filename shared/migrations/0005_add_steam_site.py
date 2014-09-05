from south.v2 import DataMigration
from django.conf import settings


class Migration(DataMigration):
    def forwards(self, orm):
        Site = orm['sites.Site']
        site, created = Site.objects.get_or_create(id=settings.SITE_ID)

        SocialApp = orm['socialaccount.SocialApp']
        provider, created = SocialApp.objects.get_or_create(provider='steam', name='Steam')
        provider.secret = ''
        provider.client_id = ''
        provider.key = settings.STEAM_API_KEY
        provider.sites.add(site)
        provider.save()
        return provider

    def backwards(self, orm):
        SocialApp = orm['socialaccount.SocialApp']
        try:
            entry = SocialApp.objects.get(provider='steam', name='Steam')
            entry.delete()
        except SocialApp.DoesNotExist:
            return

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
