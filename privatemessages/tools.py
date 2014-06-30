import copy

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now

from postman.models import Message, STATUS_PENDING, STATUS_ACCEPTED


def get_recipients(list_of_recipient_identifiers):
    return User.objects.filter(username__in=list_of_recipient_identifiers)


def create_message(recipients, options):
    default_options = {
        'auto_archive': False,
        'auto_delete': False,
        'auto_moderators': []
    }
    opt = dict(default_options.items() + options.items())

    results = []
    for recipient in recipients:
        recipient_options = copy.copy(opt)
        recipient_options['recipient'] = recipient
        result = write_message(recipient_options)
        results.append(result)
    return results


def write_message(options):
    message = Message(
        subject=options['subject'],
        body=options['body'],
        sender=options['sender'],
        recipient=options['recipient']
    )
    initial_status = message.moderation_status

    if 'auto_moderators' in options and options['auto_moderators']:
        message.auto_moderate(options['auto_moderators'])
    else:
        message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)

    if 'auto_archive' in options and options['auto_archive'] is True:
        message.sender_archived = True

    if 'auto_delete' in options and options['auto_delete'] is True:
        message.sender_deleted_at = now()

    result = message.save()

    if not 'skip_notificaton' in options or not options['skip_notification']:
        message.notify_users(initial_status, _get_site())

    return result.id


def _get_site():
    # do not require the sites framework to be installed ; and no request object is available here
    return Site.objects.get_current() if Site._meta.installed else None
