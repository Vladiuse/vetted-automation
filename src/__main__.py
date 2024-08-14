from time import sleep

from main.pages import CliniciansPage, ConvoPage

from src.main.driver import get_prod_driver, get_test_driver

# driver = get_prod_driver()
# START_URL = 'https://vettedhealth.com/backoffice/customers/stynt-healthcare/clinicians?hasMessaged=false&isLead=false&inline_conversation=true`'


driver = get_test_driver()
CLINICIAN_PAGE_TEST = "http://127.0.0.1:5500/clinicians.html"
CONVO_PAGE_TEST = "http://127.0.0.1:5500/convo.html"

# clinician_page = CliniciansPage(driver)
# clinician_page.open(CLINICIAN_PAGE_TEST)
# sleep(3)
# input('start?')
# clinician_page.send_greeting_messages()
#
#
# sleep(1)


convo_page  = ConvoPage(driver)
convo_page.open(CONVO_PAGE_TEST)
sleep(3)
convo_page.clear_filters()
sleep(2)
convo_page.transfer_convos()

input('end?')
driver.quit()
# for page_num in range(3):
#     print('Page Num:', page_num + 1)
#     clinicians_page = CliniciansPage(driver)
#     clinicians_page.open()
#     sleep(3)
#     clinicians_page.send_greeting_messages()


