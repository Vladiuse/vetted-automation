from time import sleep

from main.driver import get_test_driver
from main.pages import CliniciansPage

# driver = get_prod_driver()
# START_URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false&inline_conversation=true`'


driver = get_test_driver()
START_URL = "http://127.0.0.1:5500/index.html"
clinicians_page = CliniciansPage(driver)
clinicians_page.open(START_URL)
sleep(3)
clinicians_page.send_greeting_messages()
