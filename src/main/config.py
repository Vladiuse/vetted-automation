from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / '../.env'
STATES_PATH = BASE_DIR / '../states.json'
RECRUITERS_PATH = BASE_DIR / '../recruiters.csv'
