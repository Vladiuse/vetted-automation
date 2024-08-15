from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR.parent / '.env'
STATES_PATH = BASE_DIR.parent / 'states.json'
RECRUITERS_PATH = BASE_DIR.parent / 'recruiters.csv'
