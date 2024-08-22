import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .config import BROWSER_PROFILE_PATH, DRIVER_PATH


def get_browser_profile_path() -> str:
    return _validate_browser_profile_path(path=BROWSER_PROFILE_PATH)


def get_driver_path() -> str:
    return _validate_driver_path(path=DRIVER_PATH)


def _validate_driver_path(path: str) -> str | None:
    path = path.strip()
    if path == '':
        return None
    if not os.path.exists(path):
        raise ValueError('DRIVER_PATH does not exists')
    return path


def _validate_browser_profile_path(path: str) -> str:
    if path == '':
        raise ValueError('BROWSER_PROFILE_PATH cant be blank')
    if not os.path.exists(path):
        raise ValueError('BROWSER_PROFILE_PATH does not exists')
    if not os.path.isdir(path):
        raise ValueError('BROWSER_PROFILE_PATH must be directory')
    return path


def get_test_driver() -> webdriver.Firefox:
    service_kwargs = {}
    driver_path = get_driver_path()
    if driver_path:
        service_kwargs['executable_path'] = driver_path
    service = webdriver.FirefoxService(
        service_args=['--profile-root', os.getenv('TEST_PROFILE_PATH')],
        **service_kwargs,
    )
    driver = webdriver.Firefox(
        service=service,
    )
    return driver


def get_prod_driver() -> webdriver.Firefox:
    options = Options()
    options.profile = get_browser_profile_path()
    service_kwargs = {}
    driver_path = get_driver_path()
    if driver_path:
        service_kwargs['executable_path'] = driver_path
    service = webdriver.FirefoxService(
        **service_kwargs,
    )
    driver = webdriver.Firefox(
        service=service,
        options=options,
    )
    return driver
