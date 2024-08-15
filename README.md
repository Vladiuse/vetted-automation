# Vetted Automation

## Getting Started

To run this project, follow the steps below:

### Prerequisites

- Install [Python3.11](https://www.python.org/downloads/release/python-3119/) and Poetry on your system.
- to install Poetry open PowerShell and insert command
  `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`

### Installation

1. Configure .env
   Make copy of .env-example and call it .env. After char `=` and fill it with the
   appropriate data.
    - `BROWSER_PROFILE_PATH`: specify the path to your browser profile
    - `DRIVER_PATH`: specify the path to browser driver
    - `ACTION_PER_PAGE_LIMIT`: specify count of conversation will created on page before page reload
    - `LICENSE_STATE_SEARCH`: US states codes to search clinicians in chosen states.
      One or few codes separated by comma. Leave it blank to search in all states.
      Actual state codes you can find in `states.json`.

2. Configure active recruiters.
   To set a list recruiters you want to transfer conversation with clinicians, edit recruiters.csv.
   For convenience of editing you can open this file in Excel.
   To make recruiter active, set column `Is Active` to 1, to make not active - 0.
   To add new recruiter just add new row with name and active status.

### Usage

1. To run program open project directory in PowerShell and run command:
   ```
   poetry run python src/__main__.py
   ```
2. To stop program you can just close browser or press CTRL+C in PowerShell.