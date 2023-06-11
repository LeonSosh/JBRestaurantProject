from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ["*"]

STATICFILES_DIRS = [os.path.join(BASE_DIR, "..", "static")]
