from django.http import HttpResponseRedirect
from notif.models import Blacklist


def blacklist(request):
  if 'email' in request.GET:
    black = Blacklist(email=request.GET['email'])
    try:
      black.save()
    except:
      pass
  return HttpResponseRedirect('/')