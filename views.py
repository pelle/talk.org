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

import os
import logging

from google.appengine.api import users

import django
from django import http
from django import shortcuts
from django.utils import simplejson
from django.http import HttpResponse
from django.template import loader, Context


def respond(request, user, template, params=None):
  """Helper to render a response, passing standard stuff to the response.

  Args:
    request: The request object.
    user: The User object representing the current user; or None if nobody
      is logged in.
    template: The template name; '.html' is appended automatically.
    params: A dict giving the template parameters; modified in-place.

  Returns:
    Whatever render_to_response(template, params) returns.

  Raises:
    Whatever render_to_response(template, params) raises.
  """
  logging.debug('views.respond %s, %s, %s, %s' % 
               (request, user, template, params))
  
  if params is None:
    params = {}
  
  if user:
    params['user'] = user
    params['sign_out'] = users.CreateLogoutURL('/')
    params['is_admin'] = (users.IsCurrentUserAdmin() and
                          'Dev' in os.getenv('SERVER_SOFTWARE'))
  else:
    params['sign_in'] = users.CreateLoginURL(request.path)
    
  if not template.endswith('.html'):
    template += '.html'
  logging.info('template: %s' % template)
    
  # Send the host.
  params['HOST'] = request.get_host()
    
  # Sets a BUILD_VERSION variable for the templates to use.
  # Default to production and then set to development if we're local.
  BUILD = 'production'
  if 'Dev' in os.getenv('SERVER_SOFTWARE'):
    BUILD = 'development'
  params['BUILD'] = BUILD
  
  # Sets the CURRENT_VERSION_ID for file fingerprinting.
  params['CURRENT_VERSION_ID'] = os.getenv('CURRENT_VERSION_ID')
  
  # HTML is our default output.
  output = 'html'
  
  # We can override it.
  if request.has_key('output'):
    output = request['output'] 
    
  # HTML is our default output.
  if output == 'html':
    base_template = 'base.html'
  else:
    base_template = 'base_%s.html' % output
    
  params['base_template'] = base_template
  params['output'] = output
  logging.info('base_template: %s' % base_template)
  logging.info('output: %s' % output)
  
  # Output JSON straight away if it's what's asked for.
  if output == 'json':
    return HttpResponse(simplejson.dumps(params))

    
  # Change the headers for RSS
  elif output == 'rss':
    response = HttpResponse(mimetype='application/xhtml+xml')
    t = loader.get_template(template)
    return HttpResponse(t.render(Context(params)))

  # Otherwise, render the template normally
  else:
    return shortcuts.render_to_response(template, params)


def static(request, template):
  """Static template handler."""
  template = 'static/' + template
  user = users.GetCurrentUser()
  return respond(request, user, template)

