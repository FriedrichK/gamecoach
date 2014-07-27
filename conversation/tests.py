from mock import patch

from postman.models import Message

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.http import HttpResponse
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime
    now = datetime.now

from shared.testing.factories.account import create_accounts, create_account
from conversation.tools import create_message, retrieve_message, update_message, delete_message, InvalidSenderException, InvalidRecipientException, NoMessageSubjectException, NoMessageBodyException, MessageDoesNotExistException, MessageAccessDeniedException

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


class ToolsTestCase(TestCase):

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
