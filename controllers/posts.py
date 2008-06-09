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
from google.appengine.api import memcache
from google.appengine.api import datastore_errors

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
#  try:
#    posts = memcache.get("latest_posts")
#  except:
#    logging.error("Error happened when loading 'latest_posts' from cache")
#    memcache.delete("latest_posts")
#    posts=None
#   
#  if not posts :
  posts = Post.gql("ORDER BY created DESC LIMIT 20").fetch(20)
#    logging.info("setting memcache latest_posts")
#    memcache.set("latest_posts",posts)

  form = PostForm(None)
  if request.has_key('output') and request['output']=='ajax':
    return views.respond(request, user, 'posts/_post_list',
                         {'posts': posts})
  return views.respond(request, user, 'posts/index',
                       {'posts': posts, 'form' : form})
  


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
    profile=Profile.For(user)
  post.owner = user
  post.author = profile
  post.put()
  profile.increase_count()
  
  memcache.delete("latest_posts")
  memcache.delete("posts_from_%s"%profile.nick)
  logging.info('Saved the post, %s' % post)
  return http.HttpResponseRedirect('/')

def show(request,key):
  """Request / -- show all posts."""
  user = users.GetCurrentUser()
  try:
    post=Post.get(db.Key(unquote(key)))
    if post is None:
      return http.HttpResponseNotFound("No Post exists with that key")
    return views.respond(request, user, 'posts/show',
                       {'post': post})
  except(db.BadKeyError):
    return http.HttpResponseNotFound("No Post exists with that key")
    



def edit(request, key):
  """Edit a post.  GET shows a blank form, POST processes it."""
  user = users.GetCurrentUser()
  if user is None:
    return http.HttpResponseForbidden('You must be signed in to add or edit a post')

  post = None
  if key:
    post=Post.get(db.Key(unquote(key)))
    if post is None:
      return http.HttpResponseNotFound("No Post exists with that key")
    if post.author.user!=user:
      return http.HttpResponseForbidden('You can only edit your own posts')
  form = PostForm(data=request.POST or None, instance=post)

  if not request.POST:
    return views.respond(request, user, 'posts/edit', {'form': form, 'post': post})

  errors = form.errors
  if not errors:
    try:
      post = form.save(commit=False)
    except ValueError, err:
      errors['__all__'] = unicode(err)
  if errors:
    return views.respond(request, user, 'posts/edit', {'form': form, 'post': post})

  post.put()

  return http.HttpResponseRedirect('/')

def destroy(request, key):
  user = users.GetCurrentUser()
  if user is None:
    return http.HttpResponseForbidden('You must be signed in to add or edit a post')

  post = None
  if key:
    post=Post.get(db.Key(unquote(key)))
    if post is None:
      return http.HttpResponseNotFound("No Post exists with that key")
    if post.author.user!=user:
      return http.HttpResponseForbidden('You can only delete your own posts')

  post.delete()
  profile=Profile.For(user)
  profile.increase_count(-1)
  return http.HttpResponseRedirect('/')
