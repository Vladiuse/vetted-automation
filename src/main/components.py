import random

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .exceptions import NoSuchRecruiterInForm
from .recruiters import Recruiters


class ClinicalConversationForm:
    LOCATOR = (By.CSS_SELECTOR, 'form:has(div > textarea)',)
    MESSAGE_BOX_LOCATOR = (By.TAG_NAME, 'textarea',)
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button:has(img[src="/images/icons/send.svg"])',)

    def __init__(self, form: WebElement, driver: Firefox):
        self.form = form
        self.driver = driver

    @property
    def message_box(self) -> WebElement:
        return WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MESSAGE_BOX_LOCATOR),
        )

    @property
    def submit_button(self) -> WebElement:
        return self.form.find_element(*self.SUBMIT_BUTTON_LOCATOR)

    def insert_message(self, message: str) -> None:
        self.message_box.send_keys(message)

    def submit(self) -> None:
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", self.submit_button)
        self.submit_button.click()


class ClinicalStartMessageButton:
    LOCATOR = (By.CSS_SELECTOR, 'a[data-tooltip-id="message-button-null"]',)

    def __init__(self, message_button: WebElement, driver: Firefox):
        self.message_button = message_button
        self.driver = driver

    def open_conversation(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.message_button),
        )
        self.driver.execute_script("arguments[0].scrollIntoView();", self.message_button)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", self.message_button)
        self.message_button.click()


class ConversationSideBarToggleButton:
    LOCATOR = (By.CSS_SELECTOR, 'button[class*="recruiter-profile-pane"]',)


class ConversationSideBarBlock:
    LOCATOR = (By.CSS_SELECTOR, 'div.transform.top-12',)


class LoginFormButton:
    LOCATOR = (By.XPATH, "//button[contains(text(), 'Send Login Link')]",)


class OpenTransferFromButton:
    LOCATOR = (By.CSS_SELECTOR, "div.gap-2.hidden > button",)


class TransferForm:
    LOCATOR = (By.CSS_SELECTOR, 'form:not([class])',)
    INPUT_LOCATOR = (By.CSS_SELECTOR, 'input.rw-dropdownlist-search',)
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]',)

    def __init__(self, form: WebElement, driver: Firefox, recruiters: Recruiters):
        self.driver = driver
        self.form = form
        self.recruiters = recruiters

    @property
    def input(self) -> WebElement:
        return self.form.find_element(*self.INPUT_LOCATOR)

    @property
    def submit_button(self) -> WebElement:
        return self.form.find_element(*self.SUBMIT_BUTTON_LOCATOR)

    def get_options(self) -> list[WebElement]:
        return self.form.find_elements(By.CSS_SELECTOR, 'div[role="option"]')

    def get_option_by_recruiter_name(self, recruiter_name: str) -> WebElement:
        options = self.get_options()
        option_to_return = None
        for option in options:
            option_text = option.get_attribute("innerText").replace('*', '')
            option_text = option_text.lower()
            if option_text == recruiter_name.lower():
                option_to_return = option
                break
        if option_to_return is None:
            raise NoSuchRecruiterInForm
        return option_to_return

    def get_random_option(self) -> WebElement:
        available_recruiters_names = self.recruiters.get_active_rec_names()
        available_recruiters_names = list(map(lambda name: name.lower(), available_recruiters_names))
        options = self.get_options()
        options_to_chose = []
        for option in options:
            option_text = option.get_attribute("innerText").replace('*', '')
            option_text = option_text.lower()
            if option_text in available_recruiters_names:
                options_to_chose.append(option)
        choice = random.choice(options_to_chose)
        return choice

    def submit(self) -> None:
        self.submit_button.click()

    def chose_recruiter_by_name(self, name: str) -> None:
        option = self.get_option_by_recruiter_name(name)
        self.driver.execute_script("arguments[0].scrollIntoView();", option)
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", option)

    def chose_random_recruiter(self) -> None:
        option = self.get_random_option()
        self.driver.execute_script("arguments[0].scrollIntoView();", option)
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", option)


class ClinicalConversation:
    LOCATOR = (By.CSS_SELECTOR, 'div.group div[role="tab"]',)


class ConversationsFilterOpenButton:
    LOCATOR = (By.CSS_SELECTOR, 'button:has(img[src="/images/icons/filter.svg"])',)


class ConversationsFilterForm:
    LOCATOR = (By.CSS_SELECTOR, 'form[class*=modal-header-height]',)
    SUBMIT_BUTTON_LOCATOR = (By.CSS_SELECTOR, 'button[type="submit"]',)
    CHECKBOXES_LOCATORS = (
        (By.ID, 'checkbox-Engaged',),
        (By.ID, 'checkbox-Awaiting Reply',),
    )

    def __init__(self, form: WebElement, driver: Firefox):
        self.form = form
        self.driver = driver

    @property
    def check_boxes(self) -> list[WebElement]:
        check_boxes = []
        for locator in self.CHECKBOXES_LOCATORS:
            checkbox = self.driver.find_element(*locator)
            check_boxes.append(checkbox)
        return check_boxes

    def __off_checkboxes(self) -> None:
        for checkbox in self.check_boxes:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(checkbox),
            )
            checkbox.click()

    def clear_and_submit(self) -> None:
        self.__off_checkboxes()
        submit_button = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON_LOCATOR),
        )
        submit_button.click()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", submit_button)
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.form),
        )


class EmptyConversationListImage:
    LOCATOR = (By.CSS_SELECTOR, 'div.group img[src="/images/clipart/messages-empty-icon.svg"]',)


class ModalBlock:
    LOCATOR = (By.CSS_SELECTOR, 'div[id*="headlessui-dialog-panel"]',)


class SupportChatOpenButton:
    LOCATOR = (By.CSS_SELECTOR, 'div.intercom-lightweight-app',)
