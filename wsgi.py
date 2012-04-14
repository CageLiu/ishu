import sys
import os

sys.path.append('/var/www/mysite')
os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings' #项目名.settings

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler() 
