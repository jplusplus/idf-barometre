from .settings import *

DEBUG = False
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = (
    "app.barometre.compress_filter.CustomCssAbsoluteFilter",
    # Activate CSS minifier
    "compressor.filters.cssmin.CSSMinFilter",
)


ALLOWED_HOSTS = [".iledefrance.fr"]