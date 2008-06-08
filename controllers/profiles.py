import os
import logging
from urllib import unquote
from google.appengine.api import users

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import django
from django import http
from django import shortcuts

import views

from models import Post
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
  logging.info('Got profile, %s' % profile.nick)
  posts=profile.post_set;
  return views.respond(request, user, 'profiles/show',
                       {'posts': posts, 'profile' : profile})
                       
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
