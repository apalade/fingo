import const
from django.contrib.auth.models import User
from django.core.cache import cache
from friends.models import Friends
from news.models import News
from profile.templatetags import prettyuser
import random
import util

prof = util.Prof

__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"

def notifications(request):
  vars = {}
  if request.user.is_authenticated():
    #print traceback.print_stack()
    vars['notif'] = util.get_notifications(request.user.get_profile().notif)
  return vars

def fb_app_id(request):
  return {'fb_app_id': const.FbConst.APP_ID, 'full_url_prefix': const.FULL_URL_PREFIX}

def news_scroll(request):
  text = cache.get('news_scroll')
  if text is None:
    prof.start('news-scroll-no-cache')
    # Hit the database baby - Uh.
    text = []
    friendships = Friends.objects.filter(accepted=True).order_by('-modified_on')[:const.NewsConst.Scroll.NEW_FRIEND_MAX]
    for friendship in friendships:
      text.append(const.NewsConst.Scroll.NEW_FRIEND %
                  (
                  '/' + util.escape_html(friendship.friend.username),
                  prettyuser.user_or_first_name(friendship.friend),
                  '/' + util.escape_html(friendship.user.username),
                  prettyuser.user_or_first_name(friendship.user)))

    gossips = News.objects.filter(about_id__isnull=False).order_by('-time')[:const.NewsConst.Scroll.NEW_GOSSIP_MAX]
    for gossip in gossips:
      if gossip.anonymous:
        text.append(const.NewsConst.Scroll.NEW_GOSSIP_ANONYMOUS %
                  (
                  '/' + util.escape_html(gossip.about_id.username),
                  util.escape_html(prettyuser.user_or_first_name(gossip.about_id)),
                  '/profile/?n=' + util.escape_html(str(gossip.id)),
                  util.escape_html(gossip.title)
                  ))
      else:
        text.append(const.NewsConst.Scroll.NEW_GOSSIP %
                    (
                    '/' + util.escape_html(gossip.user.username),
                    util.escape_html(prettyuser.user_or_first_name(gossip.user)),
                    '/' + util.escape_html(gossip.about_id.username),
                    util.escape_html(prettyuser.user_or_first_name(gossip.about_id)),
                    '/profile/?n=' + util.escape_html(str(gossip.id)),
                    util.escape_html(gossip.title)
                    ))
    new_users = User.objects.order_by('-date_joined')[:const.NewsConst.Scroll.NEW_USER_MAX]
    for new_user in new_users:
      text.append(const.NewsConst.Scroll.NEW_USER %
                  (
                  '/' + util.escape_html(new_user.username),
                  util.escape_html(prettyuser.user_or_first_name(new_user)),
                  ))
    
    # Save it in cache for 30 seconds
    cache.set('news_scroll', text, 30)
    prof.stop('news-scroll-no-cache')
    
  # Randomize it each time
  random.shuffle(text)
  return {'news_scroll': text}