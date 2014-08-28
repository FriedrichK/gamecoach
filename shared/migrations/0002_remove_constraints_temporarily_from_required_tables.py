from south.v2 import SchemaMigration
from south.db import db


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.alter_column(u'profiles_profilepicture', 'user_id', self.gf('django.db.models.fields.IntegerField')(unique=False, blank=True, null=True))
        db.alter_column(u'profiles_gamecoachprofile', 'user_id', self.gf('django.db.models.fields.IntegerField')(unique=False, blank=True, null=True))
        db.alter_column(u'postman_message', 'sender_id', self.gf('django.db.models.fields.IntegerField')(unique=False, blank=True, null=True))
        db.alter_column(u'postman_message', 'recipient_id', self.gf('django.db.models.fields.IntegerField')(unique=False, blank=True, null=True))

    models = {
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'socialaccount.socialaccount': {
            'Meta': {'unique_together': "(('provider', 'uid'),)", 'object_name': 'SocialAccount'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'extra_data': ('allauth.socialaccount.fields.JSONField', [], {'default': "'{}'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'socialaccount.socialtoken': {
            'Meta': {'unique_together': "(('app', 'account'),)", 'object_name': 'SocialToken'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['socialaccount.SocialAccount']"}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['socialaccount.SocialApp']"}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.TextField', [], {}),
            'token_secret': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'socialaccount.socialapp': {
            'Meta': {'object_name': 'SocialApp'},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'account.emailaddress': {
            'Meta': {'object_name': 'EmailAddress'},
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'verbose_name': '(\'e-mail address\')'}),
            'verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'account.emailconfirmation': {
            'Meta': {'object_name': 'EmailConfirmation'},
            'email_address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['account.emailaddress']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'profiles.gamecoachprofile': {
            'Meta': {'object_name': 'GamecoachProfile'},
            'availability': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 11, 0, 0)', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mentor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mentoring': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'regions': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 11, 0, 0)', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.user']", 'unique': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'profiles.profilepicture': {
            'Meta': {'object_name': 'ProfilePicture'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2014, 8, 26, 0, 0)', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'postman.message': {
            'Meta': {'object_name': 'Message'},
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': True, 'blank': True}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': True, 'blank': True}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': True}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postman.message']", 'null': True, 'blank': True}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postman.message']", 'null': True, 'blank': True}),
            'sent_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now()'}),
            'read_at': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now()'}),
            'read_at': ('django.db.models.fields.DateField', [], {'null': True, 'blank': True}),
            'replied_at': ('django.db.models.fields.DateField', [], {'null': True, 'blank': True}),
            'sender_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient_archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sender_deleted_at': ('django.db.models.fields.DateField', [], {'null': True, 'blank': True}),
            'recipient_deleted_at': ('django.db.models.fields.DateField', [], {'null': True, 'blank': True}),
            'moderation_status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'default': '"p"'}),
            'moderation_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.user']", 'null': 'True', 'blank': 'True'}),
            'moderation_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now()'}),
            'moderation_reason': ('django.db.models.fields.CharField', [], {'max_length': '120', 'blank': 'True'})
        }
    }

    def backwards(self, orm):
        pass

    complete_apps = ['shared']
