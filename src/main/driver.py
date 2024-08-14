import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

load_dotenv('../.env')


def get_browser_profile_path():
    path = os.getenv('BROWSER_PROFILE_PATH')
    return _validate_browser_profile_path(path)


def get_driver_path():
    path = os.getenv('DRIVER_PATH')
    return _validate_driver_path(path)


def _validate_driver_path(path):
    if not path:
        raise ValueError('DRIVER_PATH cant be None or blank')
    if not os.path.exists(path):
        raise ValueError('DRIVER_PATH does not exists')
    return path


def _validate_browser_profile_path(path):
    if not path:
        raise ValueError('BROWSER_PROFILE_PATH cant be None or blank')
    if not os.path.exists(path):
        raise ValueError('BROWSER_PROFILE_PATH does not exists')
    if not os.path.isdir(path):
        raise ValueError('BROWSER_PROFILE_PATH must be directory')
    return path


def get_test_driver():
    service = webdriver.FirefoxService(
        service_args=['--profile-root', '/home/vlad/firefox_profiles'],
    )
    driver = webdriver.Firefox(
        service=service,
    )
    return driver


def get_prod_driver():
    options = Options()
    options.profile = get_browser_profile_path()
    service = webdriver.FirefoxService(
        executable_path=get_driver_path(),
    )
    driver = webdriver.Firefox(
        service=service,
        options=options,
    )
    return driver
