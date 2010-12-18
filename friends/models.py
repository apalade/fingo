from django.contrib.auth.models import User
from django.db import models


class Friends(models.Model):
  user = models.ForeignKey(User, related_name="user")
  friend = models.ForeignKey(User, related_name="friend")
  accepted = models.BooleanField(default=False)
  ignored = models.BooleanField(default=False)
  added_on = models.DateTimeField(auto_now_add=True)
  modified_on = models.DateTimeField(auto_now=True)

  def __str__(self):
    return '"%s" cu "%s"' % (self.user, self.friend)