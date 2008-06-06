# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Bootstrap for running a Django app under Google App Engine.

The site-specific code is all in other files: settings.py, urls.py,
models.py, views.py.  And in fact, only 'settings' is referenced here
directly -- everything else is controlled from there.

"""

# Standard Python imports.
import os
import sys
import logging
import __builtin__

# Google App Hosting imports.
from google.appengine.ext.webapp import util

import pickle
sys.modules['cPickle'] = pickle

# Enable info logging by the app (this is separate from appserver's
# logging).
logging.getLogger().setLevel(logging.INFO)

# Force sys.path to have our own directory first, so we can import from it.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Must set this env var *before* importing any part of Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Make sure we can import Django.  We may end up needing to do this
# little dance, courtesy of Google third-party versioning hacks.  Note
# that this patches up sys.modules, so all other code can just use
# "from django import forms" etc.
try:
  from django import v0_96 as django
except ImportError:
  pass

# Import the part of Django that we use here.
import django.core.handlers.wsgi

def main():
  # Create a Django application for WSGI.
  application = django.core.handlers.wsgi.WSGIHandler()

  # Run the WSGI CGI handler with that application.
  util.run_wsgi_app(application)

if __name__ == '__main__':
  main()
