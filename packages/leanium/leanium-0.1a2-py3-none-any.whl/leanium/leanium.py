import selenium
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

clickable = EC.element_to_be_clickable
ffwe = webdriver.firefox.webelement.FirefoxWebElement
find_one_by_name = ffwe.find_element_by_name
find_one_by_class = ffwe.find_element_by_class_name

def get_driver():
    '''get a Firefox webdriver instance'''
    driver = webdriver.Firefox()
    driver.set_window_size(1680, 1050)
    return driver

def try_to_type(elem, data):
    '''attempt to type keys into a form. Fail if the form can't be interacted with
       `data` is the string of keys to typei
       `elem` is the FirefoxWebElement to type into'''
    try:
        elem.send_keys(data)
    except ElementNotInteractableException:
        print(f'failed to type {data}')

def try_to_find(condition, find_by, query, timeout, driver):
    '''search for something by any method (key) in `search_map`.
    Returns a FirefoxWebElement if successful, otherwise None
    `find_by` is any key name in `search_map`
    `query` is the value that `find_by` should look for
    `timeout` is number of seconds (int)
    `driver` is the current webdriver instance'''
    search_map = {'id': By.ID,
                  'name': By.NAME,
                  'xpath': By.XPATH,
                  'link_text': By.LINK_TEXT,
                  'partial_link_text': By.PARTIAL_LINK_TEXT,
                  'tag_name': By.TAG_NAME,
                  'class_name': By.CLASS_NAME,
                  'css_selector': By.CSS_SELECTOR}
    if find_by not in search_map.keys():
        print('error: the specified `find_by` value {find_by} was invalid')
        sys.exit(1)
    try:
        elem = WebDriverWait(driver, timeout).until(
            condition((search_map[find_by], query))
        )
    except TimeoutException:
        print(f'unable to find {name} before {timeout}-second timeout')
    else:
        return elem

def try_to_click(elem):
    '''try to click a FirefoxWebElement. Fails if the element is not interactable'''
    try:
        ffwe.click(elem)
    except ElementNotInteractableException:
        print('failed to click element')


def find_child(parent, find_x_by, query):
    '''find the child element of `parent` based on `find_x_by`
    `find_x_by` is any class method of FirefoxWebElement that begins with "find".
        Leanium aliases those class methods, e.g. `find_one_by_class`.
    `query` is the parameter used by `find_x_by` to search child items of `parent`.'''
    try:
        child = find_x_by(parent, query)
    except NoSuchElementException:
        print(f'failed to find element {query}')
    else:
        return child
