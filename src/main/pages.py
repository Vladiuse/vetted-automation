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
    ConversationSideBarBlock,
    ConversationSideBarToggleButton,
    LoginFormButton,
    ModalBlock,
    OpenTransferFromButton,
    SupportChatOpenButton,
    TransferForm,
)
from .config import ACTION_PER_PAGE_LIMIT
from .exceptions import ActionLimitError, EmptyCliniciansList, EmptyCovnoList, NeedAuthentication
from .recruiters import Recruiters
from .vetted import get_clinicians_url, get_conversation_url


class Page:
    ERRORS_LIMITS = 2

    def __init__(self, driver: Firefox):
        self.driver = driver
        self.action_counter = 0
        self.error_counter = 0

    def open(self, *, url: str | None = None) -> None:
        if url is None:
            url = self.url
        self.driver.get(url)
        self._wait_page_load_full()

        if not self.is_authenticated:
            raise NeedAuthentication

    def _wait_page_load_full(self) -> None:
        pass

    def __check_action_counter(self) -> None:
        if self.action_counter >= ACTION_PER_PAGE_LIMIT:
            raise ActionLimitError

    def up_action_counter(self) -> None:
        self.action_counter += 1
        self._clean_error_counter()
        self.__check_action_counter()

    def up_error_counter(self, error: Exception) -> None:
        self.error_counter += 1
        self.__check__error_counter(error)

    def _clean_error_counter(self) -> None:
        self.error_counter = 0

    def __check__error_counter(self, error: Exception) -> None:
        if self.error_counter >= self.ERRORS_LIMITS:
            raise error

    @property
    def is_authenticated(self) -> bool:
        try:
            self.driver.find_element(*LoginFormButton.LOCATOR)
            return False
        except NoSuchElementException:
            return True


class CliniciansPage(Page):

    def __init__(self, driver: Firefox):
        super().__init__(driver=driver)
        self.url = get_clinicians_url()

    GREETING_MESSAGE = ('Hi! I came across your profile on Vetted and wanted to discuss potential opportunities.'
                        ' Please let me know when you would be available to discuss.')

    def send_greeting_messages(self) -> None:
        while True:
            try:
                clinician = self.__get_clinician()
                self.__send_greeting_message(clinician)
                self.up_action_counter()
            except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException,) as error:
                self.up_error_counter(error)
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
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(ConversationSideBarBlock.LOCATOR),
        )


class ConvoPage(Page):

    def __init__(self, driver: Firefox, recruiters: Recruiters):
        super().__init__(driver=driver)
        self.recruiters = recruiters
        self.url = get_conversation_url()

    def _wait_page_load_full(self) -> None:
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(SupportChatOpenButton.LOCATOR),
        )

    def clear_filters(self) -> None:
        open_filter_btn_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ConversationsFilterOpenButton.LOCATOR),
        )
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", open_filter_btn_elem)
        open_filter_btn_elem.click()
        filter_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(ConversationsFilterForm.LOCATOR),
        )
        filter_form = ConversationsFilterForm(filter_form_elem, self.driver)
        filter_form.clear_n_submit()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(ModalBlock.LOCATOR),
        )

    def transfer_conversation(self) -> None:
        while True:
            try:
                convo = self.__get_conversation()
                self.transfer_conversation_to_recruiter(convo)
                self.up_action_counter()
            except (TimeoutException, StaleElementReferenceException, ElementClickInterceptedException,) as error:
                self.up_error_counter(error)
            except (EmptyCovnoList, ActionLimitError,):
                break

    def __get_conversation(self) -> WebElement:
        try:
            conversation = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(ClinicalConversation.LOCATOR),
            )
        except TimeoutException:
            raise EmptyCovnoList
        return conversation

    def transfer_conversation_to_recruiter(self, conversation: WebElement) -> None:
        conversation.click()
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation)
        transfer_btn_elem = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(OpenTransferFromButton.LOCATOR),
        )
        self.driver.execute_script("arguments[0].style.backgroundColor = 'red';", transfer_btn_elem)
        transfer_btn_elem.click()
        transfer_form_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(TransferForm.LOCATOR),
        )
        transfer_from = TransferForm(transfer_form_elem, self.driver, self.recruiters)
        transfer_from.chose_random_recruiter()
        transfer_from.submit()
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(ModalBlock.LOCATOR),
        )
        self.driver.execute_script("arguments[0].remove();", conversation)
