 # -*- coding: utf-8 -*-

import const
from django.db.models import F
import facebook
import json
from notif.models import Notif
import subprocess
from util import Prof as prof


__all__ = ['NotificationSystem', 'FacebookSystem', 'InviteSystem']

class NotificationSystem:
  @staticmethod
  def create(user, type, extra_data={}):
    # Email notification
    prof.start('create-notif-email')
    try:
      notif = Notif(email=user.email, 
                    type=type,
                    extra_data=json.dumps(extra_data))
      notif.save()
    except:
      # TODO: log here
      raise
    prof.stop('create-notif-email')

    # User notification
    prof.start('create-notif-user')
    try:
      profile = user.get_profile()
      profile.notif |= type
      profile.save()
    except:
      # TODO: log here
      raise
    prof.stop('create-notif-user')

  @staticmethod
  def receipt(user, type):
    if 0 == type:
      # Nothing to update...
      return
    try:
      prof.start('receipt-notif')
      profile = user.get_profile()
      # TODO: race condition here?
      new_notif = profile.notif & ~type
      if new_notif != profile.notif:
        profile.notif = new_notif
        profile.save(force_update=True)
    except:
      # TODO: log here
      raise
    prof.stop('receipt-notif')

class FacebookSystem:
  @staticmethod
  def post_to_wall(cookies, body, attachment, to='me'):
    fb_user = facebook.get_user_from_cookie(cookies, const.FbConst.APP_ID, const.FbConst.APP_SECRET)
    if fb_user is None:
      return
    prof.start('fb-post')
    graph = facebook.GraphAPI(fb_user['access_token'])
    body = body.encode('utf8')
    graph.put_wall_post(body, attachment)
    prof.stop('fb-post')


  @staticmethod
  def post_new_user_to_wall(cookies):
    body = u" este în centrul atenției pe Fingo.ro!"
    attachment = {
      'name': 'Cea mai intrigantă rețea socială din România',
      'link': const.FULL_URL_PREFIX,
      'caption': "{*actor*} s-a înscris pe Fingo.ro",
      'description': "Vrei să afli care sunt cele mai noi bârfe din orașul tău? Ai o bârfă nemaipomenită și vrei s-o faci cunoscută? Hai în comunitatea Fingo!",
      'picture': 'http://fingo.ro:81/images/sigla75x75.gif',
    }
    FacebookSystem.post_to_wall(cookies, body, attachment)


  @staticmethod
  def post_gossip_to_wall(cookies, news, to='me'):
    attachment = {
      'name': 'Noutăți de pe Fingo.ro',
      'link': 'http://fingo.ro',
      'caption': "{*actor*} a scris o nouă bârfă pe Fingo.ro",
      'description': "Fingo.ro - cele mai noi bârfe din comunitatea ta",
      'picture': 'http://fingo.ro:81/images/sigla75x75.gif',
    }
    body = u' a scris despre %s: \n%s...\nrestul pe %s/profile?n=%d' \
      % (
         news.about_id.first_name if news.about_id else news.about_name,
         news.text[:const.FbConst.WALL_MSG_LENGTH],
         const.FULL_URL_PREFIX,
         news.id,
         )
    FacebookSystem.post_to_wall(cookies, body, attachment)
  
  @staticmethod
  def post_gossip_to_wall_old(cookies, news, to='me'):
    fb_user = facebook.get_user_from_cookie(cookies, const.FbConst.APP_ID, const.FbConst.APP_SECRET)
    if fb_user is None:
      return
    url = 'https://api.facebook.com/method/stream.publish?access_token='
    attachment = {
      'name': 'Noutati de pe Fingo.ro',
      'link': 'http://fingo.ro',
      'caption': "{*actor*} a scris o noua barfa pe Fingo.ro",
      #'description': "Noua barfa poate sa te intereseze direct. Intra pe reteaua sociala Fingo.ro sa vezi despre ce e vorba.",
      'picture': 'http://fingo.ro/static/logo.jpg',
    }
    action_links = [{'text': 'Share', 'href': 'http://google.ro'}]
    body = ''
    body += ' a scris despre '
    body += news.about_id.first_name if news.about_id else news.about_name
    body += ': \n'
    body += news.text[:const.FbConst.WALL_MSG_LENGTH]
    body += '[...]\n   restul pe http://www.fingo.ro/profile?n=' + str(news.id)

    import urllib, urllib2
    url += urllib.urlencode({
                            'format': 'JSON',
                            'access_token': fb_user['access_token'],
                            'message': body,
                            'attachment': json.dumps(attachment),
                            'action_links': json.dumps(action_links)})

    print url
    print urllib2.urlopen(url, timeout=5).read()


class InviteSystem:
  @staticmethod
  def getContacts(username, password, type):
    """
    full username, password, and type (yahoo, gmail, etc.)
    """
    prof.start('inviter-get-contacts')
    proc = subprocess.Popen((const.NotifConst.Inviter.PHP_PATH, 
                            const.NotifConst.Inviter.PHP_ARGS,
                            const.NotifConst.Inviter.PATH, type, username),
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    # SECURITY: Send password to stdin through pipe
    (out, err) = proc.communicate(password)
    try:
      proc.kill()
    except:
      pass
    
    if out in ('', 'false'):
      # Probably wrong credentials or provider changed communication parameters
      return None

    contacts = []
    dict = json.loads(out);
    for key in dict.keys():
      contacts.append((key, dict[key]))
    prof.stop('inviter-get-contacts')
    return contacts

  @staticmethod
  def invite(email, extra_data={}):
    """
    Send an invitation to this mail with this extra_data
    TODO: maybe we should do a bulk operation?
    """
    # Email
    prof.start('inviter-add')
    notif = Notif(email=email,
                  type=const.NotifConst.INVITE,
                  extra_data=json.dumps(extra_data))
    notif.save()
    prof.stop('inviter-add')
    