from postman.models import Message, STATUS_ACCEPTED

from django.contrib.sites.models import Site
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from shared.tools import serialize_datetime


def _get_site():
    # do not require the sites framework to be installed ; and no request object is available here
    return Site.objects.get_current() if Site._meta.installed else None


def create_message(sender, recipient, subject, body='', skip_notification=False, auto_archive=False, auto_delete=False, auto_moderators=None):
    if not user_is_valid(sender):
        raise InvalidSenderException()
    if not user_is_valid(recipient):
        raise InvalidRecipientException()
    if subject is None or subject == '':
        raise NoMessageSubjectException('this message has an empty subject line. Messages without subject cannot be sent')
    if body is None or body == '':
        raise NoMessageBodyException('this message has an empty message body. Empty message cannot be sent')
    message = Message(subject=subject, body=body, sender=sender, recipient=recipient)
    initial_status = message.moderation_status
    if auto_moderators:
        message.auto_moderate(auto_moderators)
    else:
        message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)
    if auto_archive:
        message.sender_archived = True
    if auto_delete:
        message.sender_deleted_at = now()
    message.save()
    if not skip_notification:
        message.notify_users(initial_status, _get_site())
    return message


def retrieve_message(user, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        raise MessageDoesNotExistException('message cannot be found')
    if not user_is_valid(user) or (not user == message.sender and not user == message.recipient and not user.is_superuser):
        raise MessageAccessDeniedException('access to this message is denied')
    return {
        'thread_id': message.thread_id,
        'sender': message.sender.id,
        'recipient': message.recipient.id,
        'subject': message.subject,
        'body': message.body,
        'sent_at': serialize_datetime(message.sent_at),
        'read_at': serialize_datetime(message.read_at),
        'replied_at': serialize_datetime(message.replied_at)
    }


def update_message(user, message_id, body=None, skip_notification=None, auto_archive=None, auto_delete=None, auto_moderators=None):
    message = Message.objects.get(id=message_id)
    if not user == message.sender and not user.is_superuser:
        raise MessageAccessDeniedException('you are not the original author of this message. You cannot edit it')
    if not user_is_valid(message.sender):
        raise InvalidSenderException()
    if not body is None:
        message.body = body
    if not skip_notification is None:
        message.skip_notification = skip_notification
    if not auto_archive is None:
        message.auto_archive = auto_archive
    if not auto_delete is None:
        message.auto_delete = auto_delete
    if not auto_moderators is None:
        message.auto_moderators = auto_moderators
    message.save()
    return message


def user_is_valid(user):
    if user is None or not user.is_active:
        return False
    return True


class MessageDoesNotExistException(Exception):
    pass


class MessageAccessDeniedException(Exception):
    pass


class InvalidSenderException(Exception):
    pass


class InvalidRecipientException(Exception):
    pass


class NoMessageBodyException(Exception):
    pass


class NoMessageSubjectException(Exception):
    pass
