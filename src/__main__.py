from src.main.config import RECRUITERS_PATH
from src.main.driver import get_prod_driver, get_test_driver
from src.main.pages import CliniciansPage, ConvoPage
from src.main.recruiters import Recruiters, get_recruiters_data

recruiters_data = get_recruiters_data(RECRUITERS_PATH)
recruiters = Recruiters()
recruiters.feed_from_raw_data(recruiters_data)

driver = get_prod_driver()
CLINICIAN_PAGE_TEST = "http://127.0.0.1:5500/clinicians.html"
CONVO_PAGE_TEST = "http://127.0.0.1:5500/convo.html"



for i in range(100):
    clinician_page = CliniciansPage(driver)
    clinician_page.open()
    clinician_page.send_greeting_messages()

    convo_page = ConvoPage(driver, recruiters, )
    convo_page.open()
    convo_page.clear_filters()
    convo_page.transfer_convos()
