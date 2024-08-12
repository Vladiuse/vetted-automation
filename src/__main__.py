from time import sleep

from main.components import Clinical, ClinicalConversationForm
from main.driver import get_test_driver
from main.exceptions import EmptyCliniciansList
from main.vetted import message_queue
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# driver = get_prod_driver()
# START_URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false&inline_conversation=true`'


driver = get_test_driver()
START_URL = "http://127.0.0.1:5500/index.html"
driver.get(START_URL)
sleep(3)
rows = driver.find_elements(*Clinical.LOCATOR)
print(len(rows), rows)
if not rows:
    raise EmptyCliniciansList
clinicians = [Clinical(elem) for elem in rows]

for i, clinical in enumerate(clinicians):
    print(clinical)
    driver.execute_script("arguments[0].style.backgroundColor = 'red';", clinical.elem)
    driver.execute_script("arguments[0].scrollIntoView();", clinical.elem)
    sleep(1)
    clinical.open_conversation()
    sleep(1)
    try:
        message_form_element = WebDriverWait(driver, 10).until(
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
    driver.execute_script("arguments[0].style.backgroundColor = 'red';", conversation_form.send_msg_btn)
    sleep(1)
    close_btn = driver.find_element(By.CSS_SELECTOR, 'button[class*="recruiter-profile-pane"]')
    close_btn.click()
    sleep(1)
input('Exit?')
