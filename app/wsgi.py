"""
WSGI config for barometre project.

This file will instanciate the virtualenv set into ./venv subdirectory.


"""
import os
from app.env import load 

# Load virtualenv dynamicly (if available)
load()

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings_prod")