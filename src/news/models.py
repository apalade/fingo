import const
from django.contrib.auth.models import User
from django.db import models
from stdimage import StdImageField

SOURCES = (
        (0, 'Fingo.ro'),
        (1, 'Aplicatie Facebook'),
        )

class News(models.Model):
  # Who posted this news
  user = models.ForeignKey(User, related_name="news_user")
  anonymous = models.BooleanField(default=False, null=False)

  # Who is this news about
  about_name = models.CharField(max_length=const.NewsConst.ABOUT_NAME_MAX_LENGTH,
                                blank=True, default="")
  about_id = models.ForeignKey(User, related_name="about_user",
                               null=True, blank=True)

  # Content of the news
  title = models.CharField(max_length=const.NewsConst.TITLE_MAX_LENGTH)
  text = models.TextField()
  video = models.URLField(max_length=const.NewsConst.LINK_MAX_LENGTH,
                          blank=True, default="")
  time = models.DateTimeField(auto_now_add=True)

  # Source of the news
  source = models.IntegerField(choices=SOURCES, null=False, default=0)

  def __str__(self):
    return "'%s' scrisa de %s" % (self.title, self.user)


class Image(models.Model):
  news = models.ForeignKey(News)
  image = StdImageField(upload_to="photos/news/",
                        blank=True, default="",
                        size=(800, 600),
                        thumbnail_size=(100, 75, True),
                        max_length=1024)

  def __str__(self):
    return self.image.url

class Vote(models.Model):
  user = models.ForeignKey(User)
  news = models.ForeignKey(News)
  positive = models.BooleanField(default=True)
  