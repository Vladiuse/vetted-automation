import os

from dotenv import load_dotenv

load_dotenv()

STATES_PATH = 'states.json'
RECRUITERS_PATH = 'recruiters.csv'
BROWSER_PROFILE_PATH = os.getenv('BROWSER_PROFILE_PATH')
DRIVER_PATH = os.getenv('DRIVER_PATH')
ACTION_PER_PAGE_LIMIT = int(os.getenv('ACTION_PER_PAGE_LIMIT'))
PREFERRED_TRAVEL_STATE = os.getenv('PREFERRED_TRAVEL_STATE')
