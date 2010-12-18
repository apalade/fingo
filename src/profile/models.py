from django.contrib.auth.models import User
from django.db import models
from stdimage import StdImageField

import const

GENDER = (
          (0, 'Male'),
          (1, 'Female'),
          )

CITY = (
        (0, 'Municipii'),
        (1, 'Orase'),
        (2, 'Rural'),
        )

class County(models.Model):
  name = models.CharField(max_length=const.CITY_MAX_LENGTH)

  def __unicode__(self):
    return self.name

class City(models.Model):
  name = models.CharField(max_length=const.CITY_MAX_LENGTH)
  county = models.ForeignKey(County)
  type = models.IntegerField(choices=CITY, null=False)

  def __unicode__(self):
    return self.name

class Profile(models.Model):
  user = models.ForeignKey(User, unique=True)

  gender = models.IntegerField(const.FormConst.Profile.GENDER,
                               choices=GENDER, blank=True, null=True)
  bday = models.DateField(const.FormConst.Profile.BDAY, null=True, blank=True)
  city_curr = models.ForeignKey(City, related_name="city_curr",
                                verbose_name=const.FormConst.Profile.CITY_CURR,
                                null=True, blank=True, default=None)
  city_home = models.ForeignKey(City, related_name="city_home",
                                verbose_name=const.FormConst.Profile.CITY_HOME,
                                null=True, blank=True, default=None)
  
  photo = StdImageField(const.FormConst.Profile.PHOTO, upload_to="photos/profile/", null=True,
                        blank=True,
                        size=(250, 800),
                        thumbnail_size=(50, 50, True),
                        max_length=1024)
  """
  photo = models.ImageField(const.FormConst.Profile.PHOTO,
                            upload_to="photos/profile/",
                            null=True, blank=True, default="photos/profile/johndoe.png")"""

  notif = models.IntegerField(blank=True, default=0)
  fb_id = models.BigIntegerField(null=False, default=-1)

  def __unicode__(self):
    return self.user.username
