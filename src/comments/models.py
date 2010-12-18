import const
from django.contrib.auth.models import User
from django.db import models
from news.models import News

class Comments(models.Model):
  user = models.ForeignKey(User)
  news = models.ForeignKey(News)

  text = models.CharField(max_length=const.NewsConst.COMMENT_MAX_LENGTH, null=False)
  time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return '%s despre comentariul "%s" cu textul "%s"' % (self.user, self.news, self.text)