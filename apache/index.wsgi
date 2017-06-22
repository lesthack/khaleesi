import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/opt/.virtualenvs/khaleesi/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/opt/www/khaleesi.unisem.mx')
sys.path.append('/opt/www/khaleesi.unisem.mx/khaleesi')

os.environ['DJANGO_SETTINGS_MODULE'] = 'khaleesi.settings'

# Activate your virtual env
activate_env=os.path.expanduser("/opt/.virtualenvs/khaleesi/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


