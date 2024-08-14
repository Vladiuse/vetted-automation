import random as r
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .exceptions import NoSuchRecruiterInForm
from .recruiters import recruiters


class ClinicalConversationForm:
    """
    https://i.imgur.com/k4pUEvZ.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'form:has(div > textarea)')

    def __init__(self, form):
        self.elem = form
        self.message_box = self.elem.find_element(By.TAG_NAME, 'textarea')
        self.send_msg_btn = form.find_element(By.CSS_SELECTOR, 'button:has(img[src="/images/icons/send.svg"])')

    def insert_message(self, message: str) -> None:
        self.message_box.send_keys(message)

    def submit(self) -> None:
        self.send_msg_btn.click()


class Clinical:
    """
    https://i.imgur.com/Cn4y2Pp.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'a[data-tooltip-id="message-button-null"]')

    def __init__(self, elem):
        self.elem = elem

    def open_conversation(self) -> None:
        self.elem.click()


class ConversationSideBarToggleBtn:
    """
    https://i.imgur.com/z3YQT7a.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'button[class*="recruiter-profile-pane"]')


class LoginFormBtn:
    """
    https://i.imgur.com/xzB6UJo.png
    """
    LOCATOR = (By.XPATH, "//button[contains(text(), 'Send Login Link')]")


class OpenTransferFromBtn:
    """
    https://i.imgur.com/pzB6etn.png
    """

    LOCATOR = (By.CSS_SELECTOR, "div.gap-2.hidden button")


class TransferForm:
    """
    https://i.imgur.com/Fb9tExC.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'form:not([class])')

    def __init__(self, elem:WebElement, driver):
        self.driver = driver
        self.elem = elem
        self.input = self.elem.find_element(By.CSS_SELECTOR, 'input.rw-dropdownlist-search')
        self.submit_btn = self.elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    def get_options(self) -> list[WebElement]:
        return self.elem.find_elements(By.CSS_SELECTOR, 'div[role="option"]')

    def get_option_by_rec_name(self, recruiter_name: str) -> WebElement:
        options = self.get_options()
        option_to_return = None
        for option in options:
            option_text = option.get_attribute("innerText").replace('*', '')
            option_text = option_text.lower()
            if option_text == recruiter_name.lower():
                option_to_return = option
                break
        if not option_to_return:
            raise NoSuchRecruiterInForm
        return option_to_return

    def get_random_option(self) -> WebElement:
        available_recruiters_names = recruiters.get_active_rec_names()
        available_recruiters_names = list(map(lambda name: name.lower(), available_recruiters_names))
        options = self.get_options()
        options_to_chose = list()
        for option in options:
            option_text = option.get_attribute("innerText").replace('*', '')
            option_text = option_text.lower()
            if option_text in available_recruiters_names:
                options_to_chose.append(option)
        choice = r.choice(options_to_chose)
        return choice

    def submit(self) -> None:
        self.submit_btn.click()

    def chose_recruiter_by_name(self, name: str) -> None:
        option = self.get_option_by_rec_name(name)
        self.driver.execute_script("arguments[0].scrollIntoView();", option)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", option)

    def chose_random_recruiter(self) -> None:
        option = self.get_random_option()
        self.driver.execute_script("arguments[0].scrollIntoView();", option)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", option)


class ClinicalConversation:
    """
    https://i.imgur.com/3JvuChI.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'div.group div[role="tab"]')


class ConvFilterOpenBtn:
    """
    https://i.imgur.com/NaPL1B4.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'button:has(img[src="/images/icons/filter.svg"])')


class ConvFilterForm:
    """
    https://i.imgur.com/w8kIHgk.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'form[class*=modal-header-height]')

    def __init__(self, elem:WebElement):
        self.elem = elem
        self.check_boxes = [
            self.elem.find_element(By.ID, 'checkbox-Engaged'),
            self.elem.find_element(By.ID, 'checkbox-Awaiting Reply'),
        ]
        self.submit_btn = self.elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    def _off_checkboxes(self) -> None:
        for checkbox in self.check_boxes:
            sleep(1.5)
            checkbox.click()

    def clear_n_submit(self) -> None:
        sleep(1)
        self._off_checkboxes()
        sleep(1)
        self.submit_btn.click()
