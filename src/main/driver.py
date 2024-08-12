from selenium import webdriver
from selenium.webdriver.firefox.options import Options


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
    options.profile = '/home/vlad/.mozilla/firefox/cpthrv54.dev-edition-default-1'
    # Указание пути к драйверу GeckoDriver, если он находится в нестандартном месте
    service = webdriver.FirefoxService(
        executable_path='/snap/bin/firefox.geckodriver',
    )

    # Создание экземпляра Firefox с указанными опциями и сервисом
    driver = webdriver.Firefox(
        service=service,
        options=options,
    )
    return driver
