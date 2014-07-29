import selenium.webdriver.support.ui as ui
from selenium.webdriver.support.ui import Select


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
