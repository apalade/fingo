from django import template

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"


register = template.Library()

@register.filter
def user_or_name(user):
  pretty = ''

  try:
    if '' == user.first_name or '' == user.last_name:
      pretty = user.username
    else:
      pretty = user.first_name + " " + user.last_name
  except:
    pass
  return pretty

@register.filter
def only_name(user):
  pretty = ''

  try:
    pretty = user.first_name + " " + user.last_name
  except:
    pass

  return pretty


@register.filter
def user_or_first_name(user):
  pretty = ''

  try:
    if '' == user.first_name:
      pretty = user.username
    else:
      pretty = user.first_name
  except:
    pass
  return pretty


  