from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
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
from .exceptions import EmptyCliniciansList, NeedAuthentication
from .messages import message_queue


class Page:
    URL = None

    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str = None, *, check_auth=True):
        if not url:
            url = self.URL
        self.driver.get(url)

        if check_auth:
            if not self.is_authenticated:
                raise NeedAuthentication

    @property
    def is_authenticated(self):
        try:
            self.driver.find_element(*LoginFormBtn.LOCATOR)
            return False
        except NoSuchElementException:
            return True


class CliniciansPage(Page):
    URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false'

    def send_greeting_messages(self):
        while True:
            try:
                clinician = self.get_clinician()
                self.send_greeting_message(clinician)
            except EmptyCliniciansList:
                break

    def get_clinician(self):
        rows = self.driver.find_elements(*Clinical.LOCATOR)
        print(len(rows), 'clinician on page')
        if not rows:
            raise EmptyCliniciansList
        clinician = Clinical(rows[0])
        return clinician

    def send_greeting_message(self, clinician: Clinical):
        print(clinician)
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

    def get_convos(self):
        convos = self.driver.find_elements(*ClinicalConversation.LOCATOR)
        print('convos', convos)
        return convos[0]

    def clear_filters(self):
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

    def transfer(self):
        input('Continue')
        convo = self.get_convos()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", convo)
        convo.click()
        sleep(1)
        input('Continue')
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
        input('Continue')
        try:
            transfer_form_elem = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(TransferForm.LOCATOR)
            )
        except TimeoutException:
            print('TimeoutException', TransferForm.LOCATOR)
            exit()
        transfer_from = TransferForm(transfer_form_elem)
        # transfer_from.input.send_keys('aaron')
        option = transfer_from.get_option()
        input('Continue')
        self.driver.execute_script("arguments[0].scrollIntoView();", option)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", option)
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", option)
