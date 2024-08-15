# Vetted Automation

## Getting Started

To run this project, follow the steps below:

### Prerequisites

- Install [Python3.11](https://www.python.org/downloads/release/python-3119/) and Poetry on your system.
- to install Poetry open PowerShell and insert command.
  `(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -`
- Install Firefox or update current Firefox browser to latest version.
- Login to vettedhealth.com in Firefox.
- download last version of geckodriver [Link](https://github.com/mozilla/geckodriver/releases)
  [Screenshot](https://i.imgur.com/lcjUluy.png)
  and save file on disc [Screenshot](https://i.imgur.com/VQSWVer.png)
  

### Installation

1. Configure .env
   Make copy of .env-example and call it .env. After char `=` and fill it with the
   appropriate data.
    - `BROWSER_PROFILE_PATH`: specify the path to your browser profile. To find path to profile, open Firefox
   and type in address bar `about:support`. In block Application Basics find row `Profile Directory` and take path of your profile.
   [Screenshot](https://i.imgur.com/x3IIUoM.png)
    - `DRIVER_PATH`: specify the path to browser driver. If its blank - will be used driver from your $PATH.
      To get path to you driver - right click on your geckodriver and copy path [Screenshot](https://i.imgur.com/3fxbiaH.png)
    - `ACTION_PER_PAGE_LIMIT`: specify count of conversation will created on page before page reload. You can set it on 20.
    - `PREFERRED_TRAVEL_STATE`: US states codes to search clinicians in chosen states.
      One or few codes separated by comma. Leave it blank to search in all states.
      Actual state codes you can find in `states.json`.

2. Configure active recruiters.
   To set a list recruiters you want to transfer conversation with clinicians, edit recruiters.csv.
   For convenience of editing you can open this file in Excel.
   To make recruiter active, set column `Is Active` to 1, to make not active - 0.
   To add new recruiter just add new row with name and active status.
3. Configure clinicians state.
   If you want create conversation only with user in some state, set variable `PREFERRED_TRAVEL_STATE` in .env file.
   For example if you need Alaska - PREFERRED_TRAVEL_STATE=AL,
   to set search on several states - PREFERRED_TRAVEL_STATE=OK,PA for Oklahoma and Pennsylvania.
   For searching in all states, leave it blank PREFERRED_TRAVEL_STATE=

### Usage

1. To run program open project directory in PowerShell and run command:
   ```
   poetry run python src/__main__.py
   ```
2. To stop program you can just close browser or press CTRL+C in PowerShell.