import json
import os

from dotenv import load_dotenv

from .config import ENV_PATH, STATES_PATH

load_dotenv(ENV_PATH)


def read_states_file(path):
    with open(path) as file:
        data = json.load(file)
    return data


def get_states_from_conf():
    states_string = os.getenv('SEARCH_IN_STATES')
    return validate_states_ids(states_string)


def validate_states_ids(states_string: str) -> list[str]:
    states_string = states_string.replace(' ', '').upper()
    states_ids = states_string.split(',')
    while '' in states_ids:
        states_ids.remove('')
    for state_id in states_ids:
        if state_id not in STATES_IDS:
            raise ValueError(f'Incorrect state id {state_id}')
    return states_ids


states_data = read_states_file(STATES_PATH)
STATES_IDS = [state['id'] for state in states_data]
