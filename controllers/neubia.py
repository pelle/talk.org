import os
import logging

import django
from django.http import HttpResponsePermanentRedirect

def redirect(request,path):
  """Redirect old talk.org blog posts"""
  return HttpResponsePermanentRedirect("http://neubia.com/archives/%s"%path)
