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

    LOCATOR = (By.CSS_SELECTOR, 'a[data-tooltip-id]')

    def __init__(self, elem):
        self.elem = elem

    def open_conversation(self):
        self.elem.click()

