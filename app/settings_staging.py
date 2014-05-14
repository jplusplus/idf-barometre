# -*- coding: utf-8 -*-
"""
Django settings for barometre project.
Packages required:
    * boto
    * django-storages
"""
from settings import *
import dj_database_url
import os

DATABASES = {
    'default' : dj_database_url.config()
}
# Enable debug for minfication
DEBUG                      = bool(os.getenv('DEBUG', False))
# Configure static files for S3
STATIC_URL                 = os.getenv('STATIC_URL')
STATIC_ROOT                = here('staticfiles')
STATICFILES_DIRS          += (here('static'),)
INSTALLED_APPS            += ('storages',)
DEFAULT_FILE_STORAGE       = 'storages.backends.s3boto.S3BotoStorage'
# Static storage
STATICFILES_STORAGE        = DEFAULT_FILE_STORAGE
# JS/CSS compressor settings
COMPRESS_ENABLED           = True
COMPRESS_ROOT              = STATIC_ROOT
COMPRESS_URL               = STATIC_URL
COMPRESS_STORAGE           = STATICFILES_STORAGE
COMPRESS_OFFLINE           = True
# Activate CSS minifier
COMPRESS_CSS_FILTERS       = (
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
)

ALLOWED_HOSTS = ["idf-barometre.herokuapp.com", ".iledefrance.fr"]

# AWS ACCESS
AWS_QUERYSTRING_AUTH       = False
AWS_ACCESS_KEY_ID          = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY      = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME    = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE      = os.getenv('AWS_S3_FILE_OVERWRITE') == "True" and True or False


COMPRESS_JS_FILTERS = (
    "compressor.filters.jsmin.JSMinFilter",
)

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL
}

COMPRESS_TEMPLATE_FILTER_CONTEXT = {
    'STATIC_URL': STATIC_URL
}

# Activate the cache, for true
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    }
}
