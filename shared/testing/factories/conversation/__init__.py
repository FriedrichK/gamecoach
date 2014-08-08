import datetime

from django.utils.timezone import now, get_current_timezone
from postman.models import Message, STATUS_REJECTED
from django.db import transaction


@transaction.commit_manually
def create_fake_conversation(user1, user2, user3, items=20):
    base_time = datetime.datetime(2014, 7, 28, 12, 0, 0, 0, get_current_timezone())
    batches = []
    flat = []

    for i in range(items):
        step_time = base_time + datetime.timedelta(hours=i)
        batch = []

        m1 = Message(sender=user1, recipient=user2, subject='subject_%s' % i, body='body_a_%s' % i, sent_at=step_time + datetime.timedelta(minutes=0))
        m1.save()
        batch.append(m1)
        flat.append(m1)

        m2 = Message(sender=user3, recipient=user1, subject='ignore', body='ignore', sent_at=step_time + datetime.timedelta(minutes=10))
        m2.save()
        batch.append(m2)
        flat.append(m2)

        m3 = Message(sender=user2, recipient=user1, subject='subject_%s' % i, body='body_b_%s' % i, sent_at=step_time + datetime.timedelta(minutes=20))
        m3.save()
        batch.append(m3)
        flat.append(m3)

        batches.append(batch)

    transaction.commit()
    return batches, flat


def set_message_deleted(user, messages, index):
    message = messages[index]  # self._reverse_index(messages, index)
    if message.sender == user:
        message.sender_deleted_at = now()
    if message.recipient == user:
        message.recipient_deleted_at = now()
    message.save()
    return message


def set_message_archived(user, messages, index):
    message = messages[index]  # self._reverse_index(messages, index)
    if message.sender == user:
        message.sender_archived = True
    if message.recipient == user:
        message.recipient_archived = True
    message.save()
    return message


def set_message_rejected_by_moderator(user, messages, index):
    message = messages[index]  # self._reverse_index(messages, index)
    message.moderation_status = STATUS_REJECTED
    message.save()
    return message
