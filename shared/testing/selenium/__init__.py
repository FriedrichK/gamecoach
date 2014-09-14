from django.conf import settings
from django.utils.importlib import import_module

import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select

from shared.testing.factories.account.user import create_user

MOCK_EMAIL_VALUE = 'test@test.com'
MOCK_USERNAME = 'Some Name'
MOCK_STEAM_ID = '12345'


def fill_textfield(selenium, selector, content):
    element = selenium.find_element_by_css_selector(selector)
    element.send_keys(content)


def change_checkbox(selenium, selector, state=True):
    element = selenium.find_element_by_css_selector(selector)
    element.click()


def select_option(selenium, selector, index):
    wait = ui.WebDriverWait(selenium, 10)
    wait.until(lambda selenium: len(selenium.find_elements_by_css_selector(selector + '>option')) > 0)
    select = Select(selenium.find_elements_by_css_selector(selector)[0])
    select.select_by_index(index)


def create_session_store():
    engine = import_module(settings.SESSION_ENGINE)
    store = engine.SessionStore()
    store.save()
    store.modfied = True
    return store


def get_as_user(selenium, live_server_url, url, user=None):
    if user is None:
        user, profile = create_user()

    session_store = create_session_store()
    session_items = session_store
    session_items['_auth_user_id'] = user.id
    session_items['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
    session_items.save()

    selenium.get(live_server_url)
    selenium.add_cookie({'name': settings.SESSION_COOKIE_NAME, 'value': session_store.session_key, "path": "/", "secure": False})
    selenium.get(url)


def fill_in_profile_form(selenium, has_terms_and_conditions=True, has_email=True):
    fill_textfield(selenium, 'input[name=name]', MOCK_USERNAME)

    fill_textfield(selenium, 'input[name="name-2"]', MOCK_STEAM_ID)
    fill_textfield(selenium, 'input[name="name-3"]', 'http://www.steam.com/12345')

    if has_email:
        fill_textfield(selenium, 'input[name=email]', MOCK_EMAIL_VALUE)
        fill_textfield(selenium, 'input[name="email-2"]', MOCK_EMAIL_VALUE)

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

    if has_terms_and_conditions:
        change_checkbox(selenium, 'input[name="i-agree-with-term-conditions"]', True)
