# tvoberi-download script

Python script to download report pages and convert them to PDFs from the [TV oberi legacy website](https://legacy.tvo.ch/).

## Requirements

- [python3](https://www.python.org/downloads/)
- [wkhtmltopdf](https://wkhtmltopdf.org/)

## Setup

- Create virtualenv
- Install requirements

```bash
# create virtualenv
$ python3 -m venv .venv
# enable virtualenv 
$ source .venv/bin/activate
# install requirements
$ pip install -r requirements.txt
```

## Run

- Activate virtualenv
- Run script

```bash
# enable virtualenv 
$ source .venv/bin/activate
# run script
./download_archive.py
```
