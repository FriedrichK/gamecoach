#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

HEADLESS = False

from unittest import skip

from django.conf import settings
from django.test import LiveServerTestCase, RequestFactory
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import ui, expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from profiles.models import GamecoachProfile

from shared.testing.factories.account.user import create_user
from shared.testing.factories.account import create_account
from shared.testing.factories.conversation import create_fake_conversation
from shared.testing import selenium as selenium_test_helper
from shared.testing.selenium import fill_textfield, change_checkbox, select_option, get_as_user, fill_in_profile_form

MOCK_MENTOR_USERNAME = 'mockUsername'

URL_FOR_MENTOR_CONTACT = '/mentor/%s/contact' % MOCK_MENTOR_USERNAME
URL_FOR_MENTOR_REGISTRATION = '/register/mentor'
URL_FOR_STUDENT_MENTOR_CHOICE = '/login/redirect/'

EXPECTED_STRING_ON_MENTOR_SEARCH_RESULT_PAGE = '<input type="hidden" id="page_name" name="page_name" value="results"/>'


class GamecoachLiveServerTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        if HEADLESS:
            cls.selenium = webdriver.PhantomJS('phantomjs')
        else:
            cls.selenium = WebDriver()
        super(GamecoachLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(GamecoachLiveServerTestCase, cls).tearDownClass()


class RegisterAsMentorTestCase(GamecoachLiveServerTestCase):

    @skip("Fails, but only when run in a suite. Investigate!")
    def test_should_fill_in_and_save_mentor_form_as_expected(self):
        user, profile = create_user()

        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_MENTOR_REGISTRATION), user=user)

        fill_in_profile_form(self.selenium)

        submit_button = self.selenium.find_element_by_css_selector('button[name=submit]')
        submit_button.click()

        profile = GamecoachProfile.objects.get(id=1)

        self.assertEqual(profile.email, selenium_test_helper.MOCK_EMAIL_VALUE, 'the email saved to the profile does not match the expected value')

    def test_should_redirect_to_form_correctly_and_forward_to_expected_page_after_form_completion(self):
        user, profile = create_user()
        self._go_to_mentor_or_student_choice_page(user)
        self._click_student_button()
        self._fill_in_and_submit_profile_form()

        element = WebDriverWait(self.selenium, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type=hidden][id=page_name][value=results]"))
        )

    def _go_to_mentor_or_student_choice_page(self, user):
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_STUDENT_MENTOR_CHOICE + "?next=/results"), user=user)

    def _click_student_button(self):
        submit_button = self.selenium.find_element_by_css_selector('a[id="mentor-signup"]')
        submit_button.click()

    def _fill_in_and_submit_profile_form(self):
        fill_in_profile_form(self.selenium)

        home_button = self.selenium.find_element_by_css_selector('.w-button.sign-up-button')
        home_button.click()


class RegisterStudentTestCase(GamecoachLiveServerTestCase):
    def test_should_redirect_to_form_correctly_and_forward_to_expected_page_after_form_completion(self):
        user, profile = create_user()
        self._go_to_mentor_or_student_choice_page(user)
        self._click_student_button()
        self._fill_in_and_submit_profile_form()

        element = WebDriverWait(self.selenium, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type=hidden][id=page_name][value=results]"))
        )

    def _go_to_mentor_or_student_choice_page(self, user):
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_STUDENT_MENTOR_CHOICE + "?next=/results"), user=user)

    def _click_student_button(self):
        submit_button = self.selenium.find_element_by_css_selector('a[id="student-signup"]')
        submit_button.click()

    def _fill_in_and_submit_profile_form(self):
        fill_in_profile_form(self.selenium)

        home_button = self.selenium.find_element_by_css_selector('.w-button.sign-up-button')
        home_button.click()


class ContactMentorTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = get_web_driver()
        super(ContactMentorTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactMentorTestCase, cls).tearDownClass()

    def test_should_show_login_page_as_expected(self):
        self.selenium.get('%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT))

        self.assertTrue('sign in with facebook' in self.selenium.page_source)
        self.assertTrue('sign in with Steam' in self.selenium.page_source)

    def test_should_show_message_hub_if_user_tries_to_contact_herself(self):
        user, profile = create_user()
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, '/mentor/%s/contact' % user.username), user=user)
        self.assertIn('InboxController', self.selenium.page_source)

    @skip("Fails, but only when run in a suite. Investigate!")
    def test_should_submit_profile_as_expected(self):
        user, profile = create_user()

        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT), user=user)

        fill_in_profile_form(self.selenium)

        home_button = self.selenium.find_element_by_css_selector('.w-button.sign-up-button')
        home_button.click()

        GamecoachProfile.objects.get(user=user)

    def test_should_throw_404_if_the_mentor_to_be_contacted_cannot_be_found(self):
        entries = create_account()
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT), user=entries['user'])
        self.assertIn('the page you are looking for can\'t be found', self.selenium.page_source)  # This will break whenever the 404 page changes, but apparently there is no clean way to check status codes (!)

    def test_should_exhibit_expected_flow_for_a_registered_user_without_profile(self):
        mentor_account = create_account()
        user, profile = create_user()

        self._go_to_mentor_profile_page(mentor_account, user)
        self._click_contact_mentor(mentor_account, user)
        self._fill_in_and_submit_profile_form()

        element = WebDriverWait(self.selenium, 3).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input[type=hidden][id=page_name][value=conversation]"))
        )

    def _go_to_mentor_profile_page(self, mentor_account, user):
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, '/mentor/%s' % mentor_account['user'].username), user=user)

    def _click_contact_mentor(self, mentor_account, user):
        home_button = self.selenium.find_element_by_css_selector('.contact-mentor-button')
        home_button.click()

    def _fill_in_and_submit_profile_form(self):
        fill_in_profile_form(self.selenium)

        home_button = self.selenium.find_element_by_css_selector('.w-button.sign-up-button')
        home_button.click()


class ConversationTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = get_web_driver()
        super(ConversationTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ConversationTestCase, cls).tearDownClass()

    def test_should_produce_expected_conversation(self):
        account1 = create_account()
        account2 = create_account()
        account3 = create_account()

        create_fake_conversation(account1['user'], account2['user'], account3['user'], items=3)

        url = self.live_server_url + '/conversation/' + account2['user'].username
        get_as_user(self.selenium, self.live_server_url, url, user=account1['user'])

        wait = ui.WebDriverWait(self.selenium, 10)

        wait.until(lambda driver: self.selenium.find_elements_by_css_selector('.message-block.ng-scope'))

        conversation_items = self.selenium.find_elements_by_css_selector('.message-block.ng-scope')

        self.assertEqual(len(conversation_items), 6)


def get_web_driver():
    if HEADLESS:
        return webdriver.PhantomJS('phantomjs')
    else:
        return WebDriver()
        #return webdriver.Chrome('/opt/chromedriver/chromedriver')


def build_mentor_contact_mock(mentor_contact_mock, user=None, page='pages/mentor_contact/mentor_contact_step1.html', context={'is_mentor': False}):
    request = build_request_mock(user)
    mentor_contact_mock.return_value = render(request, page, context)
    return mentor_contact_mock


def build_request_mock(user=None, url=URL_FOR_MENTOR_CONTACT):
    request_factory = RequestFactory()
    request = request_factory.get(url)

    if user is None:
        user = AnonymousUser()
    request.user = user

    return request


def fill_in_profile_form(selenium):
    fill_textfield(selenium, 'input[name=name]', 'Some Name')

    fill_textfield(selenium, 'input[name="name-2"]', '12345')
    fill_textfield(selenium, 'input[name="name-3"]', 'http://www.steam.com/12345')

    fill_textfield(selenium, 'input[name=email]', 'test@test.com')
    fill_textfield(selenium, 'input[name="email-2"]', 'test@test.com')

    fill_textfield(selenium, 'textarea[name="about-me"]', 'Blablabla')

    change_checkbox(selenium, 'input[name="role-13"]', True)

    select_option(selenium, 'select[name="field-4"]', 1)
    select_option(selenium, 'select[name="field-5"]', 2)
    select_option(selenium, 'select[name="field-6"]', 3)

    fill_textfield(selenium, 'input[name=field]', '1000')
    fill_textfield(selenium, 'input[name="field-2"]', '50%')
    fill_textfield(selenium, 'input[name="field-3"]', '100000')

    change_checkbox(selenium, 'input[name="region-10"]', True)

    change_checkbox(selenium, 'input[name=day][value="1"]', True)
    change_checkbox(selenium, 'input[name=time][value="2"]', True)

    change_checkbox(selenium, 'input[name=time][value="2"]', True)

    change_checkbox(selenium, 'input[name="role-22"]', True)

    change_checkbox(selenium, 'input[name="i-agree-with-term-conditions"]', True)
