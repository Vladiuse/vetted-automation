from time import sleep

from selenium.webdriver.common.by import By


class ClinicalConversationForm:
    LOCATOR = (By.CSS_SELECTOR, 'form:has(div > textarea)')

    def __init__(self, form):
        self.elem = form
        self.message_box = self.elem.find_element(By.TAG_NAME, 'textarea')
        self.send_msg_btn = form.find_element(By.CSS_SELECTOR, 'button:has(img[src="/images/icons/send.svg"])')

    def insert_message(self, message: str):
        self.message_box.send_keys(message)

    def submit(self):
        self.send_msg_btn.click()


class Clinical:
    LOCATOR = (By.CSS_SELECTOR, 'a[data-tooltip-id="message-button-null"]')

    def __init__(self, elem):
        self.elem = elem

    def open_conversation(self):
        self.elem.click()


class ConversationSideBarToggleBtn:
    LOCATOR = (By.CSS_SELECTOR, 'button[class*="recruiter-profile-pane"]')


class LoginFormBtn:
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

    def __init__(self, elem):
        self.elem = elem
        self.input = self.elem.find_element(By.CSS_SELECTOR, 'input.rw-dropdownlist-search')
        self.submit_btn = self.elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    def get_option(self, ):
        options = self.elem.find_elements(By.CSS_SELECTOR, 'div[role="option"]')
        option_to_return = None
        for option in options:
            text = option.get_attribute("innerText").replace('*', '')
            print(text)
            if text == 'Sydney Buckner':
                option_to_return = option
        print('option_to_return', option_to_return)
        return option_to_return


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

    def __init__(self, elem):
        self.elem = elem
        self.check_boxes = [
            self.elem.find_element(By.ID, 'checkbox-Engaged'),
            self.elem.find_element(By.ID, 'checkbox-Awaiting Reply'),
        ]
        self.submit_btn = self.elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    def _off_checkboxes(self):
        for checkbox in self.check_boxes:
            sleep(1.5)
            checkbox.click()


    def clear_n_submit(self):
        sleep(1)
        self._off_checkboxes()
        sleep(1)
        self.submit_btn.click()


