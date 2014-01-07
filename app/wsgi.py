"""
WSGI config for barometre project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site

VEND_DIR = "venv"

# for relative paths
here   = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
parent = lambda x: os.path.abspath(os.path.join(x, os.pardir))


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Virtualenv directory
venv = os.path.join( parent( here("") ), VEND_DIR)
# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('%s/local/lib/python2.7/site-packages' % venv)
# Add the app's directory to the PYTHONPATH
sys.path.append( here("") )
sys.path.append( parent( here("") ) )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings_prod")
# Activate your virtual env
activate_env=os.path.expanduser("%s/bin/activate_this.py" % venv)
execfile(activate_env, dict(__file__=activate_env))