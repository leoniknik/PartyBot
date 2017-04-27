"""
WSGI config for PartyBot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""


import os
import django

import os
from django.core.wsgi import get_wsgi_application
# from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PartyBot.settings")

application = get_wsgi_application()
# application = DjangoWhiteNoise(application)

import Bot.bot # bot's initialization