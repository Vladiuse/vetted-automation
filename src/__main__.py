from time import sleep

from main.driver import get_prod_driver
from main.pages import CliniciansPage, ConvoPage

driver = get_prod_driver()
CLINICIAN_PAGE_TEST = "http://127.0.0.1:5500/clinicians.html"
CONVO_PAGE_TEST = "http://127.0.0.1:5500/convo.html"

for _ in range(100):
    clinician_page = CliniciansPage(driver)
    clinician_page.open()
    sleep(3)
    clinician_page.send_greeting_messages()
    convo_page = ConvoPage(driver)
    convo_page.open()
    sleep(3)
    convo_page.clear_filters()
    sleep(2)
    convo_page.transfer_convos()
