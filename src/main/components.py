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

    LOCATOR =(By.XPATH, "//button[.//span[contains(text(), 'Transfer')]]")

class TransferForm:
    """
    https://i.imgur.com/Fb9tExC.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'form:not([class])')

    def __init__(self, elem):
        self.elem = elem
        self.input = self.elem.find_element(By.CSS_SELECTOR, 'input.rw-dropdownlist-search')
        self.submit_btn = self.elem.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

class ClinicalConversation:
    """
    https://i.imgur.com/3JvuChI.png
    """
    LOCATOR = (By.CSS_SELECTOR, 'div.group div[role="tab"]')