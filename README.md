# Khaleesi Beta
## Prerequisites ##

- python >= 2.6
- pip
- virtualenvwrapper

## Installation ##
```bash
mkvirtualenv khaleesi --no-site-packages
mkdir khaleesi
git clone https://github.com/lesthack/khaleesi.git khaleesi
cd khaleesi
workon kahleesi
pip install -r requirements.txt
```
## Creating Database ##
```bash
python manage.py migrate
```
## Creating an admin user ##
```bash
python manage.py createsuperuser
```

## Start the development server ##
```bash
python manage.py runserver
```

Open browser to http://127.0.0.1:8000

![khaleesi](https://pbs.twimg.com/media/B2GbRU7CEAAwjH7.png:large)
