from django.conf import settings
from rest_framework.settings import APISettings


USER_SETTINGS = getattr(settings, 'FAMILIAR', None)

DEFAULTS = {
    'VERSION': '3.5'
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
    'VERSION',
)

api_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
