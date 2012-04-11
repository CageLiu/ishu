import sys
import os

sys.path.append('/var/www/idushu')
os.environ['DJANGO_SETTINGS_MODULE']='idushu.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler() 
