import datetime

from mock import patch

from postman.models import Message, STATUS_REJECTED

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.timezone import now, get_current_timezone
from django.db import transaction

from shared.testing.factories.account import create_accounts, create_account
from conversation.tools import is_allowed_to_read_all_messages
from conversation.tools_message import create_message, retrieve_message, update_message, delete_message, InvalidSenderException, InvalidRecipientException, NoMessageSubjectException, NoMessageBodyException, MessageDoesNotExistException, MessageAccessDeniedException
from conversation.tools_folder import get_conversation, get_conversation_slice, get_inbox_slice

OK_VALUE = 'this is what we expect'
MOCK_MESSAGE_ID = '123'
NUMBER_OF_FAKE_USERS_GENERATED = 5  # has to be at least four

TEST_MESSAGE_SUBJECT = 'test_message_subject'
TEST_MESSAGE_BODY = 'test_message_body'
UPDATED_MESSAGE_BODY = 'updated_test_message_body'


class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    @patch('conversation.views.message_create')
    def test_forks_correctly_to_create(self, message_create_mock):
        message_create_mock.return_value = HttpResponse(OK_VALUE)
        response = self.client.post(reverse('message', args=[None]))
        self.assertEqual(response.content, OK_VALUE)

    @patch('conversation.views.message_update')
    def test_forks_correctly_to_update(self, message_update_mock):
        message_update_mock.return_value = HttpResponse(OK_VALUE)
        response = self.client.post(reverse('message', args=[MOCK_MESSAGE_ID]))
        self.assertEqual(response.content, OK_VALUE)

    @patch('conversation.views.message_retrieve')
    def test_forks_correctly_to_retrieve(self, message_retrieve_mock):
        message_retrieve_mock.return_value = HttpResponse(OK_VALUE)
        response = self.client.get(reverse('message', args=[MOCK_MESSAGE_ID]))
        self.assertEqual(response.content, OK_VALUE)

    @patch('conversation.views.message_delete')
    def test_forks_correctly_to_delete(self, message_delete_mock):
        message_delete_mock.return_value = HttpResponse(OK_VALUE)
        response = self.client.delete(reverse('message', args=[MOCK_MESSAGE_ID]))
        self.assertEqual(response.content, OK_VALUE)


class ToolsMessageTestCase(TestCase):

    def setUp(self):
        self._accounts = create_accounts(NUMBER_OF_FAKE_USERS_GENERATED, is_user=True, is_mentor=True)

    def test_creates_message_as_expected(self):
        recipient_user = self._get_user(1)
        self._create_test_message(recipient_user)
        actual = Message.objects.filter(recipient=recipient_user)[0]
        self.assertEqual(actual.body, TEST_MESSAGE_BODY)

    def test_throws_expected_exception_if_message_subject_is_empty(self):
        with self.assertRaises(NoMessageSubjectException):
            recipient_user = self._get_user(1)
            self._create_test_message(recipient_user, subject='')
            actual = Message.objects.filter(recipient=recipient_user)
            self.assertEquals(len(actual), 0)

    def test_throws_expected_exception_if_message_body_is_empty(self):
        with self.assertRaises(NoMessageBodyException):
            recipient_user = self._get_user(1)
            self._create_test_message(recipient_user, body='')
            actual = Message.objects.filter(recipient=recipient_user)
            self.assertEquals(len(actual), 0)

    def test_throws_expected_exception_if_sender_is_not_active(self):
        with self.assertRaises(InvalidSenderException):
            recipient_user = self._get_user(1)
            new_sender_account = create_account(is_active=False)
            sender_user = new_sender_account['user']
            self._create_test_message(recipient_user, sender_user=sender_user)
            self.assertEqual(True, False)

    def test_throws_expected_exception_if_recipient_is_not_active(self):
        with self.assertRaises(InvalidRecipientException):
            new_recipient_account = create_account(is_active=False)
            recipient_user = new_recipient_account['user']
            self._create_test_message(recipient_user)
            self.assertEqual(True, False)

    def test_retrieves_message_as_expected(self):
        recipient_user = self._get_user(1)
        message = self._create_test_message(recipient_user)

        actual = retrieve_message(self._get_user(0), message.id)
        self.assertEqual(actual['subject'], TEST_MESSAGE_SUBJECT)
        self.assertEqual(actual['body'], TEST_MESSAGE_BODY)

    def test_fails_to_retrieve_message_if_the_message_does_not_exist(self):
        with self.assertRaises(MessageDoesNotExistException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            actual = retrieve_message(self._get_user(0), -1)

    def test_fails_to_retrieve_message_if_user_is_neither_sender_nor_recipient(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            actual = retrieve_message(self._get_user(2), message.id)

    def test_fails_to_retrieve_message_if_user_is_sender_and_has_deleted_the_message(self):
        with self.assertRaises(MessageDoesNotExistException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            message.sender_deleted_at = now()
            message.save()
            actual = retrieve_message(self._get_user(0), message.id)
            message.sender_deleted_at = None
            message.save()

    def test_fails_to_retrieve_message_if_user_is_recipient_and_has_deleted_the_message(self):
        with self.assertRaises(MessageDoesNotExistException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            message.recipient_deleted_at = now()
            message.save()
            actual = retrieve_message(recipient_user, message.id)
            message.recipient_deleted_at = None
            message.save()

    def test_retrieves_message_as_expected_if_user_is_neither_sender_nor_recipient_but_is_superuser(self):
        recipient_user = self._get_user(1)
        message = self._create_test_message(recipient_user)

        user = self._get_user(2)
        user.is_superuser = True
        actual = retrieve_message(user, message.id)
        self.assertEqual(actual['subject'], TEST_MESSAGE_SUBJECT)
        self.assertEqual(actual['body'], TEST_MESSAGE_BODY)

    def test_updates_message_as_expected(self):
        recipient_user = self._get_user(1)
        message = self._create_test_message(recipient_user)
        updated_message = update_message(self._get_user(0), message.id, body=UPDATED_MESSAGE_BODY, skip_notification=True, auto_archive=True, auto_delete=True, auto_moderators=False)

        Message.objects.get(id=message.id)
        self.assertEqual(updated_message.body, UPDATED_MESSAGE_BODY)
        self.assertEqual(updated_message.skip_notification, True)
        self.assertEqual(updated_message.auto_archive, True)
        self.assertEqual(updated_message.auto_delete, True)
        self.assertEqual(updated_message.auto_moderators, False)

    def test_fails_to_update_message_if_message_does_not_exist(self):
        with self.assertRaises(MessageDoesNotExistException):
            updated_message = update_message(self._get_user(0), -1, body=UPDATED_MESSAGE_BODY, skip_notification=True, auto_archive=True, auto_delete=True, auto_moderators=False)

    def test_fails_to_update_message_if_user_is_not_sender(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            updated_message = update_message(self._get_user(2), message.id, body=UPDATED_MESSAGE_BODY, skip_notification=True, auto_archive=True, auto_delete=True, auto_moderators=False)

    def test_fails_to_update_message_if_user_has_deleted_the_message(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            message.sender_deleted_at = now()
            message.save()
            updated_message = update_message(self._get_user(0), message.id, body=UPDATED_MESSAGE_BODY, skip_notification=True, auto_archive=True, auto_delete=True, auto_moderators=False)

    def test_updates_message_as_expected_if_user_is_not_sender_but_can_moderate(self):
        recipient_user = self._get_user(1)
        message = self._create_test_message(recipient_user)
        user = self._get_user(2)
        user.is_superuser = True
        updated_message = update_message(user, message.id, body=UPDATED_MESSAGE_BODY, skip_notification=True, auto_archive=True, auto_delete=True, auto_moderators=False)

        Message.objects.get(id=message.id)
        self.assertEqual(updated_message.body, UPDATED_MESSAGE_BODY)
        self.assertEqual(updated_message.skip_notification, True)
        self.assertEqual(updated_message.auto_archive, True)
        self.assertEqual(updated_message.auto_delete, True)
        self.assertEqual(updated_message.auto_moderators, False)

    def test_deletes_message_as_expected_for_sender(self):
        with self.assertRaises(Message.DoesNotExist):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)

            delete_message(self._get_user(0), message.id)
            message_should_not_be_found = Message.objects.get(id=message.id, sender_deleted_at=None)

    def test_deletes_message_as_expected_for_recipient(self):
        with self.assertRaises(Message.DoesNotExist):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)

            delete_message(recipient_user, message.id)
            message_should_not_be_found = Message.objects.get(id=message.id, recipient_deleted_at=None)

    def test_fails_to_delete_message_because_it_does_not_exist(self):
        with self.assertRaises(MessageDoesNotExistException):
            delete_message(self._get_user(0), -1)

    def test_fails_to_delete_message_because_user_is_neither_sender_nor_recipient(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)

            delete_message(self._get_user(2), message.id)

    def test_fails_to_delete_message_because_user_is_inactive(self):
        with self.assertRaises(InvalidSenderException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)

            user = self._get_user(0)
            user.is_active = False
            delete_message(user, message.id)

    def test_fails_to_delete_message_because_message_is_deleted_for_sender(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            message.sender_deleted_at = now()
            message.save()
            delete_message(self._get_user(0), message.id)

    def test_fails_to_delete_message_because_message_is_deleted_for_recipient(self):
        with self.assertRaises(MessageAccessDeniedException):
            recipient_user = self._get_user(1)
            message = self._create_test_message(recipient_user)
            message.recipient_deleted_at = now()
            message.save()
            delete_message(self._get_user(1), message.id)

    def _create_test_message(self, recipient_user, sender_user=None, subject=TEST_MESSAGE_SUBJECT, body=TEST_MESSAGE_BODY):
        if sender_user is None:
            sender_user = self._get_user(0)
        return create_message(sender_user, recipient_user, subject, body=body)

    def _get_user(self, index):
        return self._accounts[index]['user']


class ToolsFolderTestCase(TestCase):

    def setUp(self):
        self._accounts = create_accounts(NUMBER_OF_FAKE_USERS_GENERATED, is_user=True, is_mentor=True)

    def test_returns_expected_conversation(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)
        user3 = self._get_user(2)

        self._write_test_message(user1, user2, 'test_conversation', '1')
        self._write_test_message(user2, user1, 'test_conversation', 'A')
        self._write_test_message(user1, user3, 'test_conversation', 'ignore')
        self._write_test_message(user1, user2, 'test_conversation', '2')
        self._write_test_message(user2, user1, 'test_conversation', 'B')
        self._write_test_message(user3, user1, 'test_conversation', 'ignore')
        self._write_test_message(user1, user2, 'test_conversation', '3')
        self._write_test_message(user2, user1, 'test_conversation', 'C')

        actual = [message.body for message in get_conversation(user1, [user2])]
        self.assertEqual(actual, ['C', '3', 'B', '2', 'A', '1'])

    def test_returns_expected_slice_of_conversation_excluding_deleted_archived_and_moderated_messages(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()
        self._set_message_deleted(user1, fake_conversation_flat, 9)  # removes body_a_3
        self._set_message_archived(user1, fake_conversation_flat, 6)  # removes body_a_2
        self._set_message_rejected_by_moderator(user1, fake_conversation_flat, 2)  # removes body_b_0

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=True, items=5)
        actual = [message.body for message in messages]

        self.assertEqual(actual, ['body_b_3', 'body_b_2', 'body_b_1', 'body_a_1', 'body_a_0'])

    def test_returns_expected_slice_of_conversation_for_multiple_conversation_partners(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)
        user3 = self._get_user(2)

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2, user3], time_anchor, older=True, items=5)
        actual = [message.body for message in messages]

        self.assertEqual(actual, ['body_b_3', 'ignore', 'body_a_3', 'body_b_2', 'ignore'])

    def test_returns_expected_slice_of_conversation_for_archived_items(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()
        self._set_message_archived(user1, fake_conversation_flat, 9)  # clears body_a_3
        self._set_message_archived(user1, fake_conversation_flat, 6)  # clears body_a_2

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=True, items=5, archived=True)
        actual = [message.body for message in messages]

        self.assertEqual(actual, ['body_a_3', 'body_a_2'])


    def test_returns_no_messages_when_mode_is_deleted(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()
        self._set_message_deleted(user1, fake_conversation_flat, 9)  # clears body_a_3
        self._set_message_deleted(user1, fake_conversation_flat, 6)  # clears body_a_2

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=True, items=5, deleted=True)
        actual = [message.body for message in messages]

        self.assertEqual(actual, [])

    def test_returns_expected_slice_of_conversation_when_mode_is_deleted_and_user_can_moderate(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)
        user1.is_superuser = True

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()
        self._set_message_deleted(user1, fake_conversation_flat, 9)  # clears body_a_3
        self._set_message_deleted(user1, fake_conversation_flat, 6)  # clears body_a_2

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=True, items=5, deleted=True)
        actual = [message.body for message in messages]

        self.assertTrue(is_allowed_to_read_all_messages(user1))
        self.assertEqual(actual, ['body_a_3', 'body_a_2'])

    def test_returns_expected_slice_of_conversation_when_requesting_items_newer_than_the_timestamp(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)

        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=False, items=5)
        actual = [message.body for message in messages]

        self.assertEqual(actual, ['body_b_6', 'body_a_6', 'body_b_5', 'body_a_5', 'body_b_4'])

    def test_returns_empty_list_when_no_message_can_be_found(self):
        user1 = self._get_user(0)
        user2 = self._get_user(1)

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        messages = get_conversation_slice(user1, [user2], time_anchor, older=True, items=5)
        actual = [message.body for message in messages]

        self.assertEqual(actual, [])

    def test_returns_expected_inbox_slice(self):
        user1 = self._get_user(0)
        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation()

        time_anchor = datetime.datetime(2014, 7, 28, 16, 0, 0, 0, get_current_timezone())

        inbox = get_inbox_slice(user1, time_anchor, older=True, items=5)
        actual = [message.sender.id for message in inbox]

        self.assertEqual(actual, [self._get_user(1).id, self._get_user(2).id])

    def test_returns_expected_inbox_slice_for_archived_items(self):
        user1 = self._get_user(0)
        fake_conversation_batched, fake_conversation_flat = self._create_fake_conversation(items=9)
        self._set_message_archived(user1, fake_conversation_flat, 1)
        self._set_message_archived(user1, fake_conversation_flat, 4)
        self._set_message_archived(user1, fake_conversation_flat, 7)

        messages = Message.objects.all().order_by('sent_at')
        for i in range(len(messages)):
            message = messages[i]
            print '%s\t%s\t%s\t%s\t%s\t%s' % (i, message.sent_at, message.sender.id, message.sender_archived, message.recipient_archived, message.body)

        time_anchor = datetime.datetime(2014, 7, 28, 14, 0, 0, 0, get_current_timezone())

        inbox = get_inbox_slice(user1, time_anchor, older=True, items=5, archived=True)
        actual = [message.sender.id for message in inbox]

        self.assertEqual(actual, [fake_conversation_flat[1].sender.id])

    def _get_user(self, index):
        return self._accounts[index]['user']

    def _write_test_message(self, sender, recipient, subject, body):
        return create_message(sender, recipient, subject, body=body)

    @transaction.commit_manually
    def _create_fake_conversation(self, items=20):
        user1 = self._get_user(0)
        user2 = self._get_user(1)
        user3 = self._get_user(2)
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

    def _set_message_deleted(self, user, messages, index):
        message = messages[index]  # self._reverse_index(messages, index)
        if message.sender == user:
            message.sender_deleted_at = now()
        if message.recipient == user:
            message.recipient_deleted_at = now()
        message.save()

    def _set_message_archived(self, user, messages, index):
        message = messages[index]  # self._reverse_index(messages, index)
        if message.sender == user:
            message.sender_archived = True
        if message.recipient == user:
            message.recipient_archived = True
        message.save()

    def _set_message_rejected_by_moderator(self, user, messages, index):
        message = messages[index]  # self._reverse_index(messages, index)
        message.moderation_status = STATUS_REJECTED
        message.save()

    def _reverse_index(self, items, index):
        return len(items) - 1 - index
