
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

class User(db.Model):
  owner = db.UserProperty()
  name = db.StringProperty(required=True)
  url = db.LinkProperty(required=True)
  description = db.StringProperty(multiline=True)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
  
class UserForm(djangoforms.ModelForm):
  class Meta:
    model = User
    exclude = ['owner', 'created', 'modified']

class Conversation(db.Model):
  owner = db.ReferenceProperty(User)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
      
class Post(db.Model):
  conversation = db.ReferenceProperty(Conversation)
  owner = db.UserProperty()
#  author = db.ReferenceProperty(User)
  body = db.StringProperty(required=True, multiline=False)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
  
class PostForm(djangoforms.ModelForm):
  class Meta:
    model = Post
    exclude = ['conversation', 'author','owner', 'created', 'modified']
