# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def index(request):
  pass

@login_required
def sent(request):
  pass

