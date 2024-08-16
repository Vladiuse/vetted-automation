import os
from time import sleep

from dotenv import load_dotenv
from selenium.common import TimeoutException
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .components import (
    ClinicalConversation,
    ClinicalConversationForm,
    ClinicalStartMessageButton,
    ConversationsFilterForm,
    ConversationsFilterOpenButton,
    ConversationSideBarToggleButton,
    LoginFormButton,
    OpenTransferFromBtn,
    TransferForm,
)
from .config import ENV_PATH
from .exceptions import ActionLimitError, EmptyCliniciansList, EmptyCovnoList, NeedAuthentication
from .recruiters import Recruiters
from .vetted import get_clinicians_url, get_convo_url

load_dotenv(ENV_PATH)


class Page:
    URL = None
    ACTION_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT'))
    ERRORS_LIMITS = 3

    def __init__(self, driver):
        self.driver = driver
        self.action_counter = 0
        self.error_counter = 0

    def open(self, *, url: str | None = None) -> None:
        if not url:
            url = self.URL
        self.driver.get(url)
        sleep(3)

        if not self.is_authenticated:
            raise NeedAuthentication

    def __check_action_counter(self):
        if self.action_counter >= self.ACTION_LIMIT:
            raise ActionLimitError

    def up_action_counter(self):
        self.action_counter += 1
        self._clean_error_counter()
        self.__check_action_counter()

    def up_error_counter(self):
        self.error_counter += 1
        self.__check__error_counter()

    def _clean_error_counter(self):
        self.error_counter = 0

    def __check__error_counter(self):
        if self.error_counter >= self.ERRORS_LIMITS:
            raise ActionLimitError  # TODO change error

    @property
    def is_authenticated(self) -> bool:
        try:
            self.driver.find_element(*LoginFormButton.LOCATOR)
            return False
        except NoSuchElementException:
            return True


class CliniciansPage(Page):
    URL = get_clinicians_url()

    GREETING_MESSAGE = ('Hi! I came across your profile on Vetted and wanted to discuss potential opportunities.'
                        ' Please let me know when you would be available to discuss.')

    def send_greeting_messages(self) -> None:
        while True:
            try:
                clinician = self.__get_clinician()
                self.__send_greeting_message(clinician)
                self.up_action_counter()
            except (TimeoutException, StaleElementReferenceException,ElementClickInterceptedException,):
                self.up_error_counter()
            except (EmptyCliniciansList, ActionLimitError,):
                break

    def __get_clinician(self) -> ClinicalStartMessageButton:
        try:
            start_message_button_elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(ClinicalStartMessageButton.LOCATOR),
            )
        except TimeoutException:
            raise EmptyCliniciansList
        clinician = ClinicalStartMessageButton(start_message_button_elem, self.driver)
        return clinician

    def __send_greeting_message(self, clinician: ClinicalStartMessageButton) -> None:
        clinician.open_conversation()
        message_form_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ClinicalConversationForm.LOCATOR),
        )
        conversation_form = ClinicalConversationForm(message_form_element, self.driver)
        message = CliniciansPage.GREETING_MESSAGE
        conversation_form.insert_message(message)
        conversation_form.submit()
        sidebar_toggle_btn = self.driver.find_element(*ConversationSideBarToggleButton.LOCATOR)
        sidebar_toggle_btn.click()
        sleep(1) # todo remove and create function to check is side bar closed
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(message_form_element),
        )


class ConvoPage(Page):
    URL = get_convo_url()

    ACTION_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT')) * 2

    def __init__(self, driver: Firefox, recruiters: Recruiters):
        super().__init__(driver)
        self.recruiters = recruiters

    def clear_filters(self) -> None:
        open_filter_btn_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ConversationsFilterOpenButton.LOCATOR),
        )
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", open_filter_btn_elem)
        open_filter_btn_elem.click()
        filter_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ConversationsFilterForm.LOCATOR),
        )
        filter_form = ConversationsFilterForm(filter_form_elem, self.driver)
        filter_form.clear_n_submit()
        sleep(1)

    def transfer_convos(self) -> None:
        while True:
            try:
                convo = self._get_convo()
                self.transfer_conv_to_recruiter(convo)
                self.up_action_counter()
            except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException,):
                self.up_error_counter()
            except (EmptyCovnoList, ActionLimitError,):
                break

    def _get_convo(self) -> WebElement:
        try:
            conversation = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(ClinicalConversation.LOCATOR),
            )
        except TimeoutException:
            raise EmptyCovnoList
        return conversation

    def transfer_conv_to_recruiter(self, conversation: WebElement) -> None:
        conversation.click()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation)
        transfer_btn_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(OpenTransferFromBtn.LOCATOR),
        )
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", transfer_btn_elem)
        transfer_btn_elem.click()
        transfer_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(TransferForm.LOCATOR),
        )
        transfer_from = TransferForm(transfer_form_elem, self.driver, self.recruiters)
        transfer_from.chose_random_recruiter()
        sleep(1)
        transfer_from.submit()
        sleep(1)
        self.driver.execute_script("arguments[0].remove();", conversation)
