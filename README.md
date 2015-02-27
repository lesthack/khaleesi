# Khaleesi Beta
## Prerequisites ##

- python >= 2.6
- pip
- virtualenvwrapper

## Setting up virtualenv ##
```bash
$ sudo apt-get install python-pip python-dev build-essential
$ sudo pip install --upgrade pip
$ pip install virtualenvwrapper
$ nano ~/.bash_profile
```
And set the following lines:

	export WORKON_HOME=$HOME/.virtualenvs
	source /usr/local/bin/virtualenvwrapper.sh

## Installation ##
```bash
$ source ~/.bash_profile
$ mkvirtualenv khaleesi --no-site-packages
$ git clone https://github.com/lesthack/khaleesi.git khaleesi
$ cd khaleesi
$ workon khaleesi
$ pip install -r requirements.txt
```

## Creating Database ##
```bash
$ python manage.py migrate
```

## Creating an admin user ##
```bash
$ python manage.py createsuperuser
```

## Start the development server ##
```bash
$ python manage.py runserver
```

Open browser to http://127.0.0.1:8000

![khaleesi](https://pbs.twimg.com/media/B2GbRU7CEAAwjH7.png:large)
