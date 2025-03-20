# NHL API pipeline

Building Python data pipeline to fetch data from NHL API, normalize it and store to database

Go CLI tool to show current standings etc..

## Local development requirements

- Python 3.9 
- Latest [Go toolchain](https://golang.org/dl/) installed
- [PostgreSQL](https://www.postgresql.org/download/)

## Getting started
- Setup [Python virtualenv](https://pypi.org/project/virtualenv/)
- activate virtual environment:
    -  > source \<venv-name\>/bin/activate



Install dependencies 
```bash
pip install -r requirements.txt
```



Add DB_URL environment variable in your python virtual env
1. Open venv `activate` script
```bash
nano <venv-name>/bin/activate
```
2. Add database connection string to the end of the file:
```bash
export DB_URL="Your connection string here"
```



Set up database schema
```bash
alembic upgrade head
```


running main.py should now fill tables with normalized data
