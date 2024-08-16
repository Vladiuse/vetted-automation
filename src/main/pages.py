import os
from time import sleep

from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
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

    def __init__(self, driver):
        self.driver = driver

    def open(self, *, url: str | None = None) -> None:
        if not url:
            url = self.URL
        self.driver.get(url)

        if not self.is_authenticated:
            raise NeedAuthentication

    @property
    def is_authenticated(self) -> bool:
        try:
            self.driver.find_element(*LoginFormButton.LOCATOR)
            return False
        except NoSuchElementException:
            return True


class CliniciansPage(Page):
    URL = get_clinicians_url()

    GREETING_MESSAGE =  ('Hi! I came across your profile on Vetted and wanted to discuss potential opportunities.'
                         ' Please let me know when you would be available to discuss.')


    def send_greeting_messages(self) -> None:
        sended_msg_count = 0
        while True:
            try:
                clinician = self.__get_clinician()
                self._send_greeting_message(clinician)
                sended_msg_count += 1
                if sended_msg_count >= self.ACTION_LIMIT:
                    raise ActionLimitError
            except (EmptyCliniciansList, ActionLimitError,):
                break

    def __get_clinician(self) -> ClinicalStartMessageButton:
        rows = self.driver.find_elements(*ClinicalStartMessageButton.LOCATOR)
        if not rows:
            raise EmptyCliniciansList
        clinician = ClinicalStartMessageButton(rows[0])
        return clinician

    def _send_greeting_message(self, clinician: ClinicalStartMessageButton) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", clinician.elem)
        sleep(1)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", clinician.elem)
        clinician.open_conversation()
        sleep(1.5)
        message_form_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ClinicalConversationForm.LOCATOR),
        )
        conversation_form = ClinicalConversationForm(message_form_element)
        message = CliniciansPage.GREETING_MESSAGE
        conversation_form.insert_message(message)
        sleep(2)
        conversation_form.submit()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation_form.send_msg_btn)
        sleep(1)
        sidebar_toggle_btn = self.driver.find_element(*ConversationSideBarToggleButton.LOCATOR)
        sidebar_toggle_btn.click()
        sleep(2)


class ConvoPage(Page):
    URL = get_convo_url()

    ACTION_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT')) * 2

    def __init__(self, driver: Firefox, recruiters: Recruiters):
        super().__init__(driver)
        self.recruiters = recruiters

    def _get_convo(self) -> WebElement:
        convos = self.driver.find_elements(*ClinicalConversation.LOCATOR)
        if not convos:
            raise EmptyCovnoList
        return convos[0]

    def transfer_convos(self) -> None:
        transfered_convo_count = 0
        while True:
            try:
                convo = self._get_convo()
                self.transfer_conv_to_recruiter(convo)
                transfered_convo_count += 1
                if transfered_convo_count >= self.ACTION_LIMIT:
                    raise ActionLimitError
            except (EmptyCovnoList, ActionLimitError,):
                break

    def clear_filters(self) -> None:
        open_filter_btn_elem = self.driver.find_element(*ConversationsFilterOpenButton.LOCATOR)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", open_filter_btn_elem)
        open_filter_btn_elem.click()
        sleep(1)
        filter_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ConversationsFilterForm.LOCATOR),
        )
        filter_form = ConversationsFilterForm(filter_form_elem)
        filter_form.clear_n_submit()

    def transfer_conv_to_recruiter(self, convo: WebElement) -> None:
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", convo)
        convo.click()
        sleep(1)
        transfer_btn_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OpenTransferFromBtn.LOCATOR),
        )
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", transfer_btn_elem)
        transfer_btn_elem.click()
        sleep(1)
        transfer_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(TransferForm.LOCATOR),
        )
        transfer_from = TransferForm(transfer_form_elem, self.driver)
        transfer_from.chose_random_recruiter()
        sleep(1)
        transfer_from.submit()
        sleep(1)
        self.driver.execute_script("arguments[0].remove();", convo)
        sleep(1)
