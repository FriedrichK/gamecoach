from postman.models import Message, STATUS_REJECTED
from django.db.models import Q

from conversation.tools import is_allowed_to_read_all_messages


def get_conversation(request_user, discussion_partners):
    validity_filters = get_filter_for_validity(request_user, discussion_partners)
    return Message.objects.filter(validity_filters).order_by('-sent_at')


def get_conversation_slice(request_user, discussion_partners, time_anchor, older=True, items=100, archived=False, deleted=False):
    if archived and deleted:
        raise ConversationCriteriaException('you are trying to retrieve messages that are both archived and deleted. That is logically impossible. Adjust your parameters')
    if deleted and not is_allowed_to_read_all_messages(request_user):
        return []

    validity_filters = get_filter_for_validity(request_user, discussion_partners, archived, deleted)
    time_filters = get_filters_for_time(time_anchor, older)

    order = '-sent_at'
    if not older:
        order = 'sent_at'

    result = Message.objects.filter(validity_filters, time_filters).order_by(order)[:items]
    if result is None:
        return []
    if older:
        return list(result)
    else:
        result = list(result)
        result.reverse()
        return result


def get_inbox_slice(request_user, time_anchor, older=True, items=100, archived=False, deleted=False):
    if deleted and not is_allowed_to_read_all_messages(request_user):
        return []

    filters = ~Q(sender=request_user, recipient=request_user)
    #filters = ~Q(sender=request_user)
    if older:
        filters &= Q(sent_at__lt=time_anchor)
    else:
        filters &= Q(sent_at__gt=time_anchor)

    if not archived:
        filters &= ~Q(recipient_archived=True)
    else:
        filters &= Q(recipient_archived=True)

    if not deleted:
        filters &= Q(recipient_deleted_at__isnull=True)
    else:
        filters &= Q(recipient_deleted_at__isnull=False)

    conversations = Message.objects.filter(filters).distinct('sender', 'recipient').order_by('sender', 'recipient', '-sent_at')[:items]

    clean_conversations = []
    recipients = []
    for conversation in conversations:
        other_user = get_other_user(request_user, conversation)
        if not other_user in recipients:
            clean_conversations.append(conversation)
            recipients.append(other_user)

    return clean_conversations


def get_other_user(request_user, conversation):
    if not conversation.sender == request_user:
        return conversation.sender
    if not conversation.recipient == request_user:
        return conversation.recipient


def get_filter_for_validity(request_user, discussion_partners, archived=False, deleted=False):
    user_is_either_sender_or_recipient = Q()
    if discussion_partners is None:
        user_is_either_sender_or_recipient = Q(recipient=request_user)
    else:
        for discussion_partner in discussion_partners:
            user_is_either_sender_or_recipient |= (Q(sender=request_user) & Q(recipient=discussion_partner)) | (Q(sender=discussion_partner) & Q(recipient=request_user))
    additional_constraints = []

    if not deleted:
        outgoing_message_is_not_deleted = ~(Q(sender=request_user) & Q(sender_deleted_at__isnull=False))
        incoming_message_is_not_deleted = ~(Q(recipient=request_user) & Q(recipient_deleted_at__isnull=False))
        additional_constraints.extend((outgoing_message_is_not_deleted, incoming_message_is_not_deleted,))
    else:
        outgoing_message_is_deleted = ~(Q(sender=request_user) & Q(sender_deleted_at__isnull=True))
        incoming_message_is_deleted = ~(Q(recipient=request_user) & Q(recipient_deleted_at__isnull=True))
        additional_constraints.extend((outgoing_message_is_deleted, incoming_message_is_deleted,))

    if not archived:
        outgoing_message_is_not_archived = ~(Q(sender=request_user) & Q(sender_archived=True))
        incoming_message_is_not_archived = ~(Q(recipient=request_user) & Q(recipient_archived=True))
        additional_constraints.extend((outgoing_message_is_not_archived, incoming_message_is_not_archived,))
    else:
        outgoing_message_is_archived = ~(Q(sender=request_user) & ~Q(sender_archived=True))
        incoming_message_is_archived = ~(Q(recipient=request_user) & ~Q(recipient_archived=True))
        additional_constraints.extend((outgoing_message_is_archived, incoming_message_is_archived,))

    if not is_allowed_to_read_all_messages(request_user):
        message_is_not_rejected = ~Q(moderation_status=STATUS_REJECTED)
        additional_constraints.append(message_is_not_rejected)

    constraints = user_is_either_sender_or_recipient
    for additional_constraint in additional_constraints:
        constraints &= additional_constraint
    return constraints


def get_filters_for_time(time_anchor, older):
    if older:
        return Q(sent_at__lt=time_anchor)
    return Q(sent_at__gt=time_anchor)


class ConversationCriteriaException(Exception):
    pass
