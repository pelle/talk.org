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

"""
Authentication module that mimics the behavior of Django's authentication
implementation.

Limitations:
 - all user permissions methods are not available (requires contenttypes)
"""

from django.http import HttpResponseRedirect
from django.template import Node

from google.appengine.api import users
from google.appengine.ext.webapp import template

register = template.create_template_register()
template.register_template_library("appengine_django.auth")


def login_required(function):
  """Implementation of Django's login_required decorator.
  
  The login redirect URL is always set to request.path
  """
  def login_required_wrapper(request, *args, **kw):
    if request.user.is_authenticated():
      return function(request, *args, **kw)
    return HttpResponseRedirect(users.create_login_url(request.path))
  return login_required_wrapper


class AuthLoginUrlsNode(Node):
  """Template node that creates an App Engine login or logout URL.
  
  If create_login_url is True the App Engine's login URL is rendered into
  the template, otherwise the logout URL.
  """
  def __init__(self, create_login_url, redirect):
    self.redirect = redirect
    self.create_login_url = create_login_url

  def render(self, context):
    if self.create_login_url:
      return users.create_login_url(self.redirect)
    else:
      return users.create_logout_url(self.redirect)


def auth_login_urls(parser, token):
  """Template tag registered as 'auth_login_url' and 'auth_logout_url'
  when the module is imported.
  
  Both tags take an optional argument that specifies the redirect URL and
  defaults to '/'.
  """
  bits = list(token.split_contents())
  if len(bits) == 2:
    redirect = bits[1]
  else:
    redirect = "/"
  login = bits[0] == "auth_login_url"
  return AuthLoginUrlsNode(login, redirect)
register.tag("auth_login_url", auth_login_urls)
register.tag("auth_logout_url", auth_login_urls)
