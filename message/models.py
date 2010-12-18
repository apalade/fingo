from django.db import models
from django.contrib.auth.models import User
import const

class Message(models.Model):
  user = models.ForeignKey(User, related_name="msg_user")
  to = models.ForeignKey(User, related_name="msg_to")
  subject = models.CharField(max_length=const.MSG_SUBJECT_MAX_LENGTH)
  text = models.TextField()
  read = models.BooleanField()
  time = models.DateTimeField()