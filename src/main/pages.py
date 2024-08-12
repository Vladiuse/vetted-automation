from time import sleep

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .components import Clinical, ClinicalConversationForm, ConversationSideBarToggleBtn, LoginFormBtn
from .exceptions import EmptyCliniciansList, NeedAuthentication
from .vetted import message_queue


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
    URl = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false'

    def send_greeting_messages(self):
        rows = self.driver.find_elements(*Clinical.LOCATOR)
        print(len(rows), rows)
        if not rows:
            raise EmptyCliniciansList
        clinicians = [Clinical(elem) for elem in rows]
        for i, clinical in enumerate(clinicians):
            print(clinical)
            self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", clinical.elem)
            self.driver.execute_script("arguments[0].scrollIntoView();", clinical.elem)
            sleep(1)
            clinical.open_conversation()
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
            conversation_form.submit()
            self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation_form.send_msg_btn)
            sleep(1)
            sidebar_toggle_btn = self.driver.find_element(*ConversationSideBarToggleBtn.LOCATOR)
            sidebar_toggle_btn.click()
            sleep(1)
