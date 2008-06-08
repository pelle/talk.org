import os
import logging

from google.appengine.api import users
from google.appengine.api import memcache

from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import django
from django import http
from django import shortcuts

import views

#from models import Conversation
from models import Post
from models import PostForm
from models import Profile

def index(request):
  """Request / -- show all posts."""
  user = users.GetCurrentUser()
  posts = memcache.get("latest_posts")
  if posts is None:
    posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 20")
#  websites = db.GqlQuery("SELECT * FROM Website ORDER BY created DESC LIMIT 5")
  form = PostForm(None)
  return views.respond(request, user, 'posts/index',
                       {'posts': posts, 'form' : form})
  

def increment_profile_post_count(profile, amount):
  if profile.postCount is None:
    postCount=amount
  else:
    profile.postCount += amount
  profile.put()


def create(request):
  """Create a post.  GET shows a blank form, POST processes it."""
  
  user = users.GetCurrentUser()
  if user is None:
    # Now make them login.
    # See what we did in websites.py - this should happen here as well.
    login_url = users.create_login_url(request.get_full_path())
    return http.HttpResponseRedirect(login_url)
    
  form = PostForm(data=request.POST or None)

  if not request.POST:
    return views.respond(request, user, 'posts/form', 
                         {'form': form})
  
    
  errors = form.errors
  if not errors:
    try:
      post = form.save(commit=False)
    except ValueError, err:
      errors['__all__'] = unicode(err)
  if errors:
    return views.respond(request, user, 'posts/form', 
                         {'form': form})
  
  profile=Profile.gql("where user=:1",user).get()
  
  if profile is None:
    profile=Profile(user=user,nick=user.nickname())
    profile.put()
  post.owner = user
  post.author = profile
  post.put()
  
  db.run_in_transaction(increment_profile_post_count, profile,1)
  
  memcache.delete("latest_posts")
  logging.info('Saved the post, %s' % post)
  return http.HttpResponseRedirect('/')


def edit(request, greeting_id):
  """Create or edit a gift.  GET shows a blank form, POST processes it."""
  user = users.GetCurrentUser()
  if user is None:
    return http.HttpResponseForbidden('You must be signed in to add or edit a greeting')

  greeting = None
  if greeting_id:
    greeting = models.posts.Greeting.get(db.Key.from_path(Greeting.kind(), int(greeting_id)))
    if greeting is None:
      return http.HttpResponseNotFound('No greeting exists with that key (%r)' %
                                       greeting_id)

  form = models.GreetingForm(data=request.POST or None, instance=greeting)

  if not request.POST:
    return views.respond(request, user, 'greeting', {'form': form, 'greeting': greeting})

  errors = form.errors
  if not errors:
    try:
      greeting = form.save(commit=False)
    except ValueError, err:
      errors['__all__'] = unicode(err)
  if errors:
    return views.respond(request, user, 'greeting', {'form': form, 'greeting': greeting})

  greeting.put()

  return http.HttpResponseRedirect('/')
