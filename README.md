# s15

## For developers

### Installation

Python packages

    pip install -r src/requirements.txt

Initial migrations

    python src/manage.py migrate

Ignoring changes in the database file

    git update-index --assume-unchanged src/db.sqlite3

Creating superuser

    python src/manage.py createsuperuser


Create environment settings

    touch src/s15/.env

### Running the app

    make dev
