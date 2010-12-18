import time

import const
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
import logging
import logging.config
import logging.handlers

__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"

# Logging
logging.config.fileConfig(const.LogConst.CONFIG)
log = logging.getLogger()
log_prof = logging.getLogger('profiling')

class Prof:
  prof = {}

  @staticmethod
  def start(key):
    if not settings.PROFILING:
      return
    
    if key in Prof.prof:
      log_prof.warning("We already have '%s' key" % (key))
    else:
      log_prof.info("%s: start" % (key))
      Prof.prof[key] = time.time()

  @staticmethod
  def stop(key):
    if not settings.PROFILING:
      return

    if key in Prof.prof:
      log_prof.info("%s: %.3f" % (key, time.time() - Prof.prof[key]))
      del Prof.prof[key]
    else:
      log_prof.warning("We do not have '%s'" % (key))


def get_user(username):
  if username is None or username == '':
    return None

  try:
    return User.objects.get(username=username)
  except User.DoesNotExist:
    return None

def get_notifications(notif):
  return {'none': notif == const.NotifConst.NONE,
    'msg': notif & const.NotifConst.MSG != 0,
    'friend_req': notif & const.NotifConst.FRIEND_REQ != 0,
    'friend_confirm': notif & const.NotifConst.FRIEND_CONFIRM != 0,
    'friend_sugg': notif & const.NotifConst.FRIEND_SUGG != 0,
    'new_comment_gossip': notif & const.NotifConst.NEW_COMMENT_GOSSIP != 0,
    'new_comment_gossip_me': notif & const.NotifConst.NEW_COMMENT_GOSSIP_ME != 0,
    'new_gossip_me': notif & const.NotifConst.NEW_GOSSIP_ME != 0,}

def get_matching_users(users, term):
  if term == '':
    return users

  terms = term.split(' ', 1)
  where = Q(Q(first_name__icontains=terms[0]) | \
            Q(last_name__icontains=terms[0]) | \
            Q(username__icontains=terms[0]))
  if len(terms) > 1:
    where = where & Q (Q(first_name__icontains=terms[1]) | \
                       Q(last_name__icontains=terms[1]) | \
                       Q(username__icontains=terms[1]))

  return users.filter(where).order_by('first_name', 'last_name', 'username')

def escape_html(html):
  return unicode(html).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def is_param_empty(key, structure):
  if key not in structure or structure[key] == '':
    return True
  return False

LOCK_MODES = (
    'ACCESS SHARE',
    'ROW SHARE',
    'ROW EXCLUSIVE',
    'SHARE UPDATE EXCLUSIVE',
    'SHARE',
    'SHARE ROW EXCLUSIVE',
    'EXCLUSIVE',
    'ACCESS EXCLUSIVE',
)


from django.db import connection
from django.db import transaction

def require_lock(model, lock):
  """
  Decorator for PostgreSQL's table-level lock functionality

  Example:
      @transaction.commit_on_success
      @require_lock(MyModel, 'ACCESS EXCLUSIVE')
      def myview(request)
          ...

  PostgreSQL's LOCK Documentation:
  http://www.postgresql.org/docs/8.3/interactive/sql-lock.html
  """
  def require_lock_decorator(view_func):
    def wrapper(*args, **kwargs):
      if lock not in LOCK_MODES:
          raise ValueError('%s is not a PostgreSQL supported lock mode.')

      cursor = connection.cursor()
      cursor.execute(
          'LOCK TABLE %s IN %s MODE' % (model._meta.db_table, lock)
      )
      return view_func(*args, **kwargs)
  
    return wrapper
  return require_lock_decorator