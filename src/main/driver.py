import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .config import ENV_PATH

load_dotenv(ENV_PATH)


def get_browser_profile_path() -> str:
    path = os.getenv('BROWSER_PROFILE_PATH')
    return _validate_browser_profile_path(path)


def get_driver_path() -> str:
    path = os.getenv('DRIVER_PATH')
    return _validate_driver_path(path)


def _validate_driver_path(path) -> str | None:
    path = path.strip()
    if not path:
        return None
    if not os.path.exists(path):
        raise ValueError('DRIVER_PATH does not exists')
    return path


def _validate_browser_profile_path(path) -> str:
    if not path:
        raise ValueError('BROWSER_PROFILE_PATH cant be None or blank')
    if not os.path.exists(path):
        raise ValueError('BROWSER_PROFILE_PATH does not exists')
    if not os.path.isdir(path):
        raise ValueError('BROWSER_PROFILE_PATH must be directory')
    return path


def get_test_driver() -> webdriver.Firefox:
    service = webdriver.FirefoxService(
        service_args=['--profile-root', os.getenv('TEST_PROFILE_PATH')],
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
