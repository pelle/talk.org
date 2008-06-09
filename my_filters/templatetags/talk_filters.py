import re
from django import template
#from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter
#@stringfilter
def atify(value):
  m=re.compile('(@([\w\.-]+))')
  return m.sub(r'<a href="/profiles/\2" class="profile" rel="friend">\1</a>',value)
atify.is_safe = True
