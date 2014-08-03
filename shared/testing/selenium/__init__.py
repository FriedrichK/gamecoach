from django.conf import settings
from django.utils.importlib import import_module

import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select

from shared.testing.factories.account.user import create_user


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
