from .settings import *

# Edit here the configuration of you're database
DATABASES = {
    'default' : {
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '', 
        'NAME': '',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

ALLOWED_HOSTS = ["localhost", ".iledefrance.fr"]

DEBUG 			 = False
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = (
    "app.barometre.compress_filter.CustomCssAbsoluteFilter",
    # Activate CSS minifier
    "compressor.filters.cssmin.CSSMinFilter",
)
