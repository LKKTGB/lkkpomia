import os

from website.settings.production import *

DEBUG = True if "DEBUG" in os.environ else False
ALLOWED_HOSTS = ["lkkpomia-stage.azurewebsites.net"]
