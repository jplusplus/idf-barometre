"""
WSGI config for barometre project.

This file will instanciate the virtualenv set into ./venv subdirectory.


"""
import os
import sys
import site

VENV_DIR = "venv"

# for relative paths
here   = lambda x="": os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
parent = lambda x: os.path.abspath(os.path.join(x, os.pardir))


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Virtualenv directory
venv = os.path.join( parent( here() ), VENV_DIR)
# If virtual env exists
if os.path.isdir(venv):     
    # Determine python packages
    major, minor = sys.version_info[0:2]
    sitepackages = '{venv}/local/lib/python{major}.{minor}/site-packages'.format(
        venv=venv,
        major=major,
        minor=minor
    )  
    # Add the site-packages of the chosen virtualenv to work with
    if os.path.isfile(sitepackages):
        site.addsitedir(sitepackages)
        # Activate your virtual env
        activate_env=os.path.expanduser("%s/bin/activate_this.py" % venv)
        execfile(activate_env, dict(__file__=activate_env))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings_prod")