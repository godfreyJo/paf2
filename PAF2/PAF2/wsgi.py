"""
WSGI config for PAF2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import sys

from dotenv import load_dotenv

# Load environment

project_folder = 'home/aketch/paf2'

load_dotenv(os.path.join(project_folder, '.env'))

# Add your project directory to the path
path = '/home/aketch/paf2/PAF2'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'PAF2.settings'


from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
