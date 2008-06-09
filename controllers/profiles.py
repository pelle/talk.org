import os
import logging
from urllib import unquote
from google.appengine.api import users

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

  posts = memcache.get("posts_from_%s"%nick)
  if posts is None:
    posts=profile.post_set
    posts.order("-created")
    posts=posts.fetch(20)
    logging.info("setting memcache posts_from_%s"%nick)
    memcache.set("posts_from_%s"%nick,posts)
  
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
