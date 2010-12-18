from django.db import models
from django.db import models
import datetime

import const

GENDER = (
          (0, 'Male'),
          (1, 'Female'),
          )

class FbNews(models.Model):
  title = models.CharField(max_length=const.NewsConst.TITLE_MAX_LENGTH)
  text = models.TextField()
  gender = models.IntegerField(choices=GENDER, null=False)
  counter_retrieved = models.IntegerField(default=0)
  counter_used = models.IntegerField(default=0)
  last_used = models.DateTimeField(default=datetime.datetime.now())
  added_on = models.DateTimeField(auto_now_add=True)


  def __unicode__(self):
    return self.title

