from django.db import connection

from south.v2 import DataMigration

DJANGO_FACEBOOK_USER_TABLE = 'django_facebook_facebookcustomuser'
DJANGO_FACEBOOK_PROFILE_TABLE = 'django_facebook_facebookprofile'


class Migration(DataMigration):

    def forwards(self, orm):
        cursor = connection.cursor()
        if not old_user_table_exists(cursor):
            return

        empty_new_tables(orm)

        user_id_mapping = {}
        users = get_all_old_user_entries(cursor)
        for user in users:
            db_user = migrate_user(orm, cursor, user)
            migrate_facebook_profile_data(orm, cursor, user, db_user)
            user_id_mapping[user[0]] = db_user

        relink_gamecoach_profiles(orm, user_id_mapping)
        relink_gamecoach_profilepictures(orm, user_id_mapping)
        relink_messages(orm, user_id_mapping)

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


def old_user_table_exists(cursor):
    table_names = connection.introspection.get_table_list(cursor)
    return DJANGO_FACEBOOK_USER_TABLE in table_names


def empty_new_tables(orm):
    EmailConfirmation = orm['account.emailconfirmation']
    EmailConfirmation.objects.all().delete()

    EmailAddress = orm['account.emailaddress']
    EmailAddress.objects.all().delete()

    SocialToken = orm['socialaccount.socialtoken']
    SocialToken.objects.all().delete()

    SocialAccount = orm['socialaccount.socialaccount']
    SocialAccount.objects.all().delete()

    User = orm['auth.user']
    User.objects.all().delete()


def get_all_old_user_entries(cursor):
    cursor.execute("SELECT * FROM %s;" % DJANGO_FACEBOOK_USER_TABLE)
    rows = cursor.fetchall()
    return rows


def migrate_user(orm, cursor, user):
    data = {
        'password': user[1],
        'last_login': user[2],
        'is_superuser': user[3],
        'username': user[4],
        'first_name': user[5],
        'last_name': user[6],
        'email': user[7],
        'is_staff': user[8],
        'is_active': user[9],
        'date_joined': user[10]
    }
    User = orm['auth.user']
    user = User(**data)
    user.save()
    return user


def migrate_facebook_profile_data(orm, cursor, user, db_user):
    old_facebook_profile_data = get_old_facebook_profile_data(cursor, user[0])
    if old_facebook_profile_data is None:
        return
    create_new_facebook_profile(orm, db_user, old_facebook_profile_data)


def get_old_facebook_profile_data(cursor, old_user_id):
    cursor.execute("SELECT * FROM %s WHERE user_id = %s;" % (DJANGO_FACEBOOK_PROFILE_TABLE, old_user_id))
    row = cursor.fetchone()
    return row


def create_new_facebook_profile(orm, db_user, old_facebook_profile_data):
    SocialAccount = orm['socialaccount.socialaccount']
    profile, created = SocialAccount.objects.get_or_create(user=db_user)
    profile.last_login = db_user.last_login
    profile.date_joined = db_user.date_joined
    profile.provider = "facebook"
    profile.uid = old_facebook_profile_data[2] if not old_facebook_profile_data[2] is None else 0
    profile.extra_data = old_facebook_profile_data[10]
    profile.save()


def relink_gamecoach_profiles(orm, user_id_mapping):
    old_gamecoach_profile_data = get_old_gamecoach_profile_data(orm)

    relinked_gameocach_profile_data = relink_gamecoach_profile_data(old_gamecoach_profile_data, user_id_mapping)

    GameCoachProfile = orm['profiles.gamecoachprofile']
    GameCoachProfile.objects.all().delete()
    for item in relinked_gameocach_profile_data:
        gamecoachprofile = GameCoachProfile(**item)
        gamecoachprofile.save()


def get_old_gamecoach_profile_data(orm):
    GamecoachProfile = orm['profiles.gamecoachprofile']
    return GamecoachProfile.objects.all().values()


def relink_gamecoach_profile_data(old_gamecoach_profile_data, user_id_mapping):
    for item in old_gamecoach_profile_data:
        old_user_id = item['user_id']
        item['user_id'] = user_id_mapping[old_user_id].id
    return old_gamecoach_profile_data


def relink_gamecoach_profilepictures(orm, user_id_mapping):
    old_gamecoach_profilepicture_data = get_old_gamecoach_profilepicture_data(orm)

    relinked_gameocach_profilepicture_data = relink_gamecoach_profilepicture_data(old_gamecoach_profilepicture_data, user_id_mapping)

    ProfilePicture = orm['profiles.profilepicture']
    ProfilePicture.objects.all().delete()
    for item in relinked_gameocach_profilepicture_data:
        gamecoachprofilepicture = ProfilePicture(**item)
        gamecoachprofilepicture.save()


def get_old_gamecoach_profilepicture_data(orm):
    ProfilePicture = orm['profiles.profilepicture']
    return ProfilePicture.objects.all().values()


def relink_gamecoach_profilepicture_data(old_gamecoach_profilepicture_data, user_id_mapping):
    for item in old_gamecoach_profilepicture_data:
        old_user_id = item['user_id']
        item['user_id'] = user_id_mapping[old_user_id].id
    return old_gamecoach_profilepicture_data


def relink_messages(orm, user_id_mapping):
    old_message_data = get_old_message_data(orm)

    relinked_message_data = relink_message_data(old_message_data, user_id_mapping)

    Message = orm['postman.message']
    Message.objects.all().delete()
    for item in relinked_message_data:
        message = Message(**item)
        message.save()


def get_old_message_data(orm):
    Message = orm['postman.message']
    return Message.objects.all().values()


def relink_message_data(old_message_data, user_id_mapping):
    for item in old_message_data:
        old_sender_id = item['sender_id']
        item['sender_id'] = user_id_mapping[old_sender_id].id

        old_recipient_id = item['recipient_id']
        item['recipient_id'] = user_id_mapping[old_recipient_id].id

    return old_message_data


class CannotRetrieveDatabaseCursorException(Exception):
    pass


class GamecoachProfileTableUserIdsNotUniqueException(Exception):
    pass
