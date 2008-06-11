"""
Talk.org - A Twitter like Application
Copyright (C) 2008 Pelle Braendgaard

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import logging
from urllib import unquote
from google.appengine.api import users
from google.appengine.api import datastore_errors

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
from google.appengine.api import memcache

import django
from django import http
from django import shortcuts

import views

from models import Post
from models import PostForm
from models import Profile
from models import ProfileForm

def index(request):
  """Request / -- show all posts."""
  user=users.GetCurrentUser()
  profiles = Profile.gql("ORDER BY postCount DESC LIMIT 20")
  return views.respond(request, user, 'profiles/index',
                       {'profiles': profiles})

def show(request, nick):
  user = users.GetCurrentUser()
  nick=unquote(nick)
  logging.info('Got key, %s' % nick)
  profile = Profile.ForNick(nick)
  if not profile:
    logging.warn('Nickname missing: %s' % nick)
    return http.HttpResponseRedirect("/profiles")
  logging.info('Got profile, %s' % profile.nick)
  
  post={}
  if profile.user!=user:
    post["body"]="@%s "%profile.nick
  else:
    post=None
  form = PostForm(post)

  posts=profile.cachedPosts()
  
  return views.respond(request, user, 'profiles/show',
                       {'posts': posts, 'profile' : profile,'form':form})
                       
def edit(request):
  user=users.GetCurrentUser()
  if user is None:
    return http.HttpResponseForbidden('You must be signed in to add or edit a greeting')
  profile=Profile.gql("where user=:1",user).get()
  form = ProfileForm(data=request.POST or None, instance=profile)

  if not request.POST:
    return views.respond(request, user, 'profiles/form', {'form': form, 'current_profile': profile})

  errors = form.errors
  if not errors:
    try:
      profile = form.save(commit=False)
    except ValueError, err:
      errors['__all__'] = unicode(err)
  if errors:
    return views.respond(request, user, 'profiles/form', {'form': form, 'current_profile': profile})

  profile.put()

  return http.HttpResponseRedirect('/')
