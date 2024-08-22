import json

from .config import PREFERRED_TRAVEL_STATE, STATES_PATH


def read_states_file(path: str) -> dict:
    with open(path) as file:
        data = json.load(file)
    return data


def get_states_from_conf() -> list:
    return validate_states_ids(PREFERRED_TRAVEL_STATE)


def validate_states_ids(states_string: str) -> list[str]:
    states_string = states_string.replace(' ', '').upper()
    states_string = states_string.strip(',')
    if states_string == '':
        return []
    states_ids = states_string.split(',')
    for state_id in states_ids:
        if state_id not in STATES_IDS:
            raise ValueError(f'Incorrect state id {state_id}')
    return states_ids


states_data = read_states_file(STATES_PATH)
STATES_IDS = [state['id'] for state in states_data]
