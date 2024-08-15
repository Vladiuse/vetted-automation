import os
from time import sleep

from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .components import (
    Clinical,
    ClinicalConversation,
    ClinicalConversationForm,
    ConversationSideBarToggleBtn,
    ConvFilterForm,
    ConvFilterOpenBtn,
    LoginFormBtn,
    OpenTransferFromBtn,
    TransferForm,
)
from .config import ENV_PATH
from .exceptions import ActionLimitError, EmptyCliniciansList, EmptyCovnoList, NeedAuthentication
from .messages import message_queue

load_dotenv(ENV_PATH)


class Page:
    URL = None

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str = None, *, check_auth=True) -> None:
        if not url:
            url = self.URL
        self.driver.get(url)

        if check_auth:
            if not self.is_authenticated:
                raise NeedAuthentication

    @property
    def is_authenticated(self) -> bool:
        try:
            self.driver.find_element(*LoginFormBtn.LOCATOR)
            return False
        except NoSuchElementException:
            return True


class CliniciansPage(Page):
    URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false'
    ACTION_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT'))

    def send_greeting_messages(self) -> None:
        sended_msg_count = 0
        while True:
            try:
                clinician = self._get_clinician()
                self._send_greeting_message(clinician)
                sended_msg_count += 1
                if sended_msg_count >= self.ACTION_LIMIT:
                    raise ActionLimitError
            except (EmptyCliniciansList, ActionLimitError):
                break

    def _get_clinician(self) -> Clinical:
        rows = self.driver.find_elements(*Clinical.LOCATOR)
        print(len(rows), 'clinician on page')
        if not rows:
            raise EmptyCliniciansList
        clinician = Clinical(rows[0])
        return clinician

    def _send_greeting_message(self, clinician: Clinical) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", clinician.elem)
        sleep(1)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", clinician.elem)
        clinician.open_conversation()
        sleep(1.5)
        try:
            message_form_element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ClinicalConversationForm.LOCATOR)
            )
        except TimeoutException:
            print('TimeoutException', ClinicalConversationForm.LOCATOR)
            exit()
        conversation_form = ClinicalConversationForm(message_form_element)
        message = message_queue.next_message()
        conversation_form.insert_message(message)
        sleep(2)
        conversation_form.submit()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation_form.send_msg_btn)
        sleep(1)
        sidebar_toggle_btn = self.driver.find_element(*ConversationSideBarToggleBtn.LOCATOR)
        sidebar_toggle_btn.click()
        sleep(2)


class ConvoPage(Page):
    URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/conversations?conversation='
    ACTION_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT'))

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
            except (EmptyCovnoList, ActionLimitError):
                break

    def clear_filters(self) -> None:
        open_filter_btn_elem = self.driver.find_element(*ConvFilterOpenBtn.LOCATOR)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", open_filter_btn_elem)
        open_filter_btn_elem.click()
        sleep(1)
        try:
            filter_form_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(ConvFilterForm.LOCATOR)
            )
        except TimeoutException:
            print('TimeoutException', ConvFilterForm.LOCATOR)
            exit()
        filter_form = ConvFilterForm(filter_form_elem)
        filter_form.clear_n_submit()

    def transfer_conv_to_recruiter(self, convo: WebElement) -> None:
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", convo)
        convo.click()
        sleep(1)
        try:
            transfer_btn_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(OpenTransferFromBtn.LOCATOR)
            )
            self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", transfer_btn_elem)
            print('transfer_btn_elem', transfer_btn_elem)
        except TimeoutException:
            print('TimeoutException', OpenTransferFromBtn.LOCATOR)
            exit()
        transfer_btn_elem.click()
        sleep(1)

        try:
            transfer_form_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(TransferForm.LOCATOR)
            )
        except TimeoutException:
            print('TimeoutException', TransferForm.LOCATOR)
            exit()
        transfer_from = TransferForm(transfer_form_elem, self.driver)
        transfer_from.chose_random_recruiter()
        sleep(1)
        transfer_from.submit()
        sleep(1)
        self.driver.execute_script("arguments[0].remove();", convo)
        sleep(1)
