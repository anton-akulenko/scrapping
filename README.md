# Bryl's python Template Project

## How to use this template (tasklist)
 - [ ] clone or download project
 - [ ] remove git connection with current repo
 - [ ] search and react to all `#TODO` and `# TODO` you will found in this project
 - [ ] clear all you will not need, especially:
   - for **non** flask app:
     - remove dirs: `static`, `templates`, `routes`
     - remove #flask section in `requirements.txt` file
   - for **non** streamlit app:
     - remove dir `.streamlit`
 - [ ] remove this section from `readme.md`
 - [ ] enjoy! 😄


## Requirements
 - #TODO: add here project requirements 
 - Python >= 3.12.1


## Installation
 - clone the project
   - create virtual env
   ```
   python3 -m venv ./venv
   ```
   - update pip
     ```
     python -m pip install --upgrade pip
     ```
   - install requirements
     - for development: 
      ```
      pip3 install -r requirements-dev.txt
      ```
     - for use/tests: 
      ```
      pip3 install -r requirements.txt
      ```
 - #TODO: add here other instructions


## Project settings
 - #TODO: add here descriptions of all project settings 


## Run
 - #TODO: add here run instructions


## Codestyle
 - use flake8
   ```
   $PyInterpreterDirectory$/flake8 $ProjectFileDir$
   ```
 - use mypy
   ```
   $PyInterpreterDirectory$/mypy --config-file $ProjectFileDir$/pyproject.toml $ProjectFileDir$
   ```
 - use black
   ```
   $PyInterpreterDirectory$/black --diff --color $ProjectFileDir$
   ```
 - use ruff
   ```
   $PyInterpreterDirectory$/ruff check $ProjectFileDir$
   ```

All configs of all linters are in the `/pyproject.toml` file.


## TODO list for future
 - [ ] #TODO: add here any information as project todo list for future improvements 

## TODO list of this project for me 
#TODO: remove this section
 - [x] Rewrite settings from tomli to dotenv
 - [ ] Add different types of apps
   - [x] Console
   - [x] Flask
   - [x] streamlit
   - [ ] GUI
 - [ ] Add comments to main code steps
