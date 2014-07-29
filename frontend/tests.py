import time

HEADLESS = False

from django.conf import settings
from django.test import LiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver

from shared.testing.selenium import fill_textfield, change_checkbox, select_option


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
