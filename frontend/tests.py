import time

HEADLESS = False

from django.conf import settings
from django.test import LiveServerTestCase, RequestFactory
from django.utils.unittest import skip
from django.shortcuts import render
from django.contrib.auth.models import AnonymousUser

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

from mock import patch

from shared.testing.factories.account.user import create_user
from shared.testing.selenium import fill_textfield, change_checkbox, select_option, get_as_user
from profiles.models import GamecoachProfile
from frontend.views import mentor_contact

MOCK_MENTOR_USERNAME = 'mockUsername'
URL_FOR_MENTOR_CONTACT = '/mentor/%s/contact' % MOCK_MENTOR_USERNAME


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
        self.selenium.find_element_by_xpath('//div[contains(@class, "login-screen") ]').click()
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


class ConversationTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        if HEADLESS:
            cls.selenium = webdriver.PhantomJS('phantomjs')
        else:
            cls.selenium = WebDriver()
        super(ConversationTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ConversationTestCase, cls).tearDownClass()

    @patch('frontend.views.mentor_contact')
    def test_should_redirect_to_home_on_logo_click(self, mentor_contact_mock):
        request_factory = RequestFactory()
        request = request_factory.get(URL_FOR_MENTOR_CONTACT)
        mentor_contact_mock.return_value = render(request, 'pages/conversation/inbox.html', {'is_mentor': False})

        self.selenium.get('%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT))

        home_button = self.selenium.find_element_by_css_selector('.w-button sign-up-button')
        home_button.click()

        self.assertTrue('Get coached by experienced gamers' in self.selenium.page_source)


class ContactMentorTestCase(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.selenium = get_web_driver()
        super(ContactMentorTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ContactMentorTestCase, cls).tearDownClass()

    @skip
    @patch('frontend.views.mentor_contact')
    def test_should_show_login_page_as_expected(self, mentor_contact_mock):
        mock_request = build_request_mock()
        mentor_contact_mock.return_value = mentor_contact(mock_request, MOCK_MENTOR_USERNAME)

        self.selenium.get('%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT))

        self.assertTrue('login with facebook' in self.selenium.page_source)
        self.assertTrue('sign up with facebook' in self.selenium.page_source)

    def test_should_submit_profile_as_expected(self):
        user, profile = create_user()

        get_as_user(self.selenium, self.live_server_url, '%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT), user=user)

        fill_in_profile_form(self.selenium)

        home_button = self.selenium.find_element_by_css_selector('.w-button.sign-up-button')
        home_button.click()

        #time.sleep(2)  # The new profile is not added instantly

        GamecoachProfile.objects.get(user=user)

    @skip
    @patch('frontend.views.mentor_contact')
    def test_should_do_something_as_expected(self, mentor_contact_mock):
        mentor_contact_mock = build_mentor_contact_mock(mentor_contact_mock, page='pages/conversation/inbox.html')

        self.selenium.get('%s%s' % (self.live_server_url, URL_FOR_MENTOR_CONTACT))

        self.assertTrue(False)


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
