from django.db import models

import const

TYPE = ((const.NotifConst.NONE, 'None'),
        (const.NotifConst.MSG, 'New Message'),
        (const.NotifConst.FRIEND_REQ, 'Friend Request'),
        (const.NotifConst.FRIEND_CONFIRM, 'Friend Confirmation'),
        (const.NotifConst.FRIEND_SUGG, 'Friend Suggestion'),
        (const.NotifConst.NEW_COMMENT_GOSSIP, 'Comment over gossip'),
        (const.NotifConst.NEW_COMMENT_GOSSIP_ME, 'Comment over a gossip about me'),
        (const.NotifConst.NEW_GOSSIP_ME, 'Gossip about me'),
        (const.NotifConst.INVITE, 'Invitation'))


class Notif(models.Model):
  email = models.EmailField(max_length=const.FormConst.EMAIL_MAX_LENGTH)
  type = models.IntegerField(choices=TYPE, null=False)
  extra_data = models.TextField() # JSON encoded data
  time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return '%s (%d)' % (self.email, self.type)

class Blacklist(models.Model):
  email = models.EmailField(max_length=const.FormConst.EMAIL_MAX_LENGTH, unique=True)
  time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.email
