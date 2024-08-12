from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .components import Clinical, ClinicalConversationForm, ConversationSideBarToggleBtn, LoginFormBtn
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
        sleep(1)
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
        sleep(1)
        # conversation_form.submit()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation_form.send_msg_btn)
        sleep(1)
        sidebar_toggle_btn = self.driver.find_element(*ConversationSideBarToggleBtn.LOCATOR)
        sidebar_toggle_btn.click()
        sleep(1)
