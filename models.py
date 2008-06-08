
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms
try:
  from django import newforms as forms
except ImportError:
  from django import forms

class Profile(db.Model):
  user = db.UserProperty()
  nick = db.StringProperty(required=True)
  fullName = db.StringProperty()
  url = db.LinkProperty()
  postCount = db.IntegerProperty(default=0)
  description = db.StringProperty(multiline=True)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
      
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
  body = db.StringProperty(required=True, multiline=False)
  created = db.DateTimeProperty(auto_now_add=True)
  modified = db.DateTimeProperty(auto_now_add=True)
  
class PostForm(djangoforms.ModelForm):
  body = forms.CharField(widget=forms.TextInput(attrs={'size':'60','maxlength':'140','label':'Talk'} ))
  class Meta:
    model = Post
    exclude = ['conversation', 'author','owner', 'created', 'modified']
