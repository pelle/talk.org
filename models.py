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
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
try:
  from django import newforms as forms
except ImportError:
  from django import forms

import logging

class Profile(db.Model):
  user = db.UserProperty(required=True)
  nick = db.StringProperty(required=True)
  fullName = db.StringProperty()
  url = db.LinkProperty()
  postCount = db.IntegerProperty(default=0)
  description = db.StringProperty(multiline=True)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
  
  def increase_count(self,amount=None):
    if amount is None:
      amount=1
    
    def increment_profile_post_count(amount):
      if self.postCount is None:
        postCount=amount
      else:
        self.postCount += amount
      self.put()
    return db.run_in_transaction(increment_profile_post_count,amount)
  
  def name(self):
    if self.fullName:
      return self.fullName;
    return self.nick;
    
  @staticmethod
  def ForNick(nick):
    logging.info("Loading Profile: %s" % nick)
    profile= Profile.get_by_key_name("Profile:%s" % nick)
    if not profile:
      logging.warn("Couldn't load Profile: %s" % nick)
    return profile
      

  @staticmethod
  def For(user=None):
    """Gets user-data in a specific category (such as "settings")
       from the database. If no user-specific data exists yet, a new
       unique entry will be created.
    """

    # If no user is given, get the user that is currently logged in.
    # If nobody is logged in, return None
    if not user:
      user = users.GetCurrentUser()
    if not user:
      return None

    # In most cases, we can just do a lookup by nick_name
    profile = Profile.ForNick(user.nickname())
    if profile and profile.user==user:
      return profile
    
    # That didn't work -- let's do a gql query, just in case the user's
    # nickname changed but we can find it by object
    by_user_profile = Profile.gql('WHERE user=:1',user).get()
    if by_user_profile:
      return by_user_profile

    # Ok, so there is nothing in the database yet. We assume that we can
    # create a new entry, using the key from above. In theory, there is a
    # slim chance of creating a duplicate object (if the user's email
    # address changes the very second we create that entry and a
    # parallel request creates a new entry with the same user), but that's
    # a chance we are willing to take.
    if profile:
      nick="%s2"%user.nickname()
    else:
      nick=user.nickname()
    profile = Profile(key_name="Profile:%s" % nick,user=user,nick=nick)
    profile.put()
    return profile
  
      
class ProfileForm(djangoforms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['nick','postCount','user', 'created', 'modified']

#class Conversation(db.Model):
#  owner = db.ReferenceProperty(Profile,collection_name=conversations)
#  created = db.DateTimeProperty(auto_now_add=True)
#  modified = db.DateTimeProperty(auto_now_add=True)
      
class Post(db.Model):
#  conversation = db.ReferenceProperty(Conversation,collection_name=posts)
  owner = db.UserProperty()
  author = db.ReferenceProperty(Profile)
  body = db.StringProperty(required=True, multiline=True)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
  
class PostForm(djangoforms.ModelForm):
  body = forms.CharField(widget=forms.Textarea(attrs={'cols':'50','rows':'3'} ))
  class Meta:
    model = Post
    exclude = ['conversation', 'author','owner', 'created', 'modified']

    from google.appengine.api import users
    from google.appengine.ext import db
