#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

HEADLESS = False

from django.conf import settings
from django.test import LiveServerTestCase, RequestFactory
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver
from selenium.webdriver.support import ui

from profiles.models import GamecoachProfile

from shared.testing.factories.account.user import create_user
from shared.testing.factories.account import create_account
from shared.testing.factories.conversation import create_fake_conversation
from shared.testing import selenium as selenium_test_helper
from shared.testing.selenium import fill_textfield, change_checkbox, select_option, get_as_user, fill_in_profile_form

MOCK_MENTOR_USERNAME = 'mockUsername'

URL_FOR_MENTOR_CONTACT = '/mentor/%s/contact' % MOCK_MENTOR_USERNAME
URL_FOR_MENTOR_REGISTRATION = '/register/mentor'


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

    def test_should_fill_in_and_save_mentor_form_as_expected(self):
        user, profile = create_user()

        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_MENTOR_REGISTRATION), user=user)

        fill_in_profile_form(self.selenium)

        submit_button = self.selenium.find_element_by_css_selector('button[name=submit]')
        submit_button.click()

        profile = GamecoachProfile.objects.get(id=1)

        self.assertEqual(profile.email, selenium_test_helper.MOCK_EMAIL_VALUE, 'the email saved to the profile does not match the expected value')


class MentorContactTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if HEADLESS:
            cls.selenium = webdriver.PhantomJS('phantomjs')
        else:
            cls.selenium = WebDriver()
        super(MentorContactTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MentorContactTestCase, cls).tearDownClass()

    def test_display(self):
        self._load_login_page()
        self._click_login_button_and_change_to_facebook_popup_dialog()
        self._submit_login_form()
        self._validate_profile_form_is_loaded()
        self._fill_in_and_submit_profile_form()

    def _load_login_page(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/mentor/fkauder/contact'))
        time.sleep(1)

    def _click_login_button_and_change_to_facebook_popup_dialog(self):
        self.selenium.find_element_by_xpath('//a[contains(@class, "sign-up-button login") ]').click()
        windows = self.selenium.window_handles
        self.selenium.switch_to_window(windows[1])

    def _submit_login_form(self):
        facebook_email = settings.FACEBOOK_TEST_USER
        facebook_pass = settings.FACEBOOK_TEST_PASSWORD

        email = self.selenium.find_element_by_name('email')
        password = self.selenium.find_element_by_name('pass')
        email.send_keys(facebook_email)
        password.send_keys(facebook_pass)
        submit = 'input[type="submit"]'
        submit = self.selenium.find_element_by_css_selector(submit)
        submit.click()

        windows = self.selenium.window_handles
        self.selenium.switch_to_window(windows[0])
        time.sleep(5)

    def _validate_profile_form_is_loaded(self):
        response = self.selenium.find_element_by_css_selector('[for=region-15]').text
        self.assertTrue('Australia' in response)

    def _fill_in_and_submit_profile_form(self):
        fill_textfield(self.selenium, 'input[name=name]', 'Some Name')

        fill_textfield(self.selenium, 'input[name="name-2"]', '12345')
        fill_textfield(self.selenium, 'input[name="name-3"]', 'http://www.steam.com/12345')

        fill_textfield(self.selenium, 'input[name=email]', 'test@test.com')
        fill_textfield(self.selenium, 'input[name="email-2"]', 'test@test.com')

        fill_textfield(self.selenium, 'textarea[name="about-me"]', 'Blablabla')

        change_checkbox(self.selenium, 'input[name="role-13"]', True)

        select_option(self.selenium, 'select[name="field-4"]', 1)
        select_option(self.selenium, 'select[name="field-5"]', 2)
        select_option(self.selenium, 'select[name="field-6"]', 3)

        fill_textfield(self.selenium, 'input[name=field]', '1000')
        fill_textfield(self.selenium, 'input[name="field-2"]', '50%')
        fill_textfield(self.selenium, 'input[name="field-3"]', '100000')

        change_checkbox(self.selenium, 'input[name="region-10"]', True)

        change_checkbox(self.selenium, 'input[name=day][value="1"]', True)
        change_checkbox(self.selenium, 'input[name=time][value="2"]', True)

        change_checkbox(self.selenium, 'input[name=time][value="2"]', True)

        change_checkbox(self.selenium, 'input[name="role-22"]', True)

        change_checkbox(self.selenium, 'input[name="i-agree-with-term-conditions"]', True)

        submit_button = self.selenium.find_element_by_css_selector('button[name=submit]')
        submit_button.click()


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

        self.assertTrue('login with facebook' in self.selenium.page_source)
        self.assertTrue('sign up with facebook' in self.selenium.page_source)

    def test_should_show_message_hub_if_user_tries_to_contact_herself(self):
        user, profile = create_user()
        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, '/mentor/%s/contact' % user.username), user=user)
        self.assertIn('InboxController', self.selenium.page_source)

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
