import time

import const
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from fb_app.models import FbNews
from news.models import News
from profile.models import Profile
from profile.views import _fb_user_to_auth
import urllib
import util

log = util.log

def index(request):
  if 'signed_request' in request.GET:
    fb_data = _parse_signed_request(request.GET['signed_request'], const.FbConst.APP_SECRET)
    if 'oauth_token' in fb_data and fb_data['expires'] > time.time():
      log.debug("fb_app data: %s" % str(fb_data))
      user = _login_in_main(request, fb_data)
      if user is None:
        return HttpResponseRedirect('/app/')

      if not request.user.is_authenticated():
        # FIXME: refactor this together with _login_in_main
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)


      response = render_to_response('fb_app/app.html',
                                {'oauth_token': fb_data['oauth_token'], 
                                'app_url': const.FbConst.APP_URL},
                                context_instance=RequestContext(request), )
      # IE fix or you'll not be able to set cookies from iframe
      response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
      return response
  response = render_to_response('fb_app/redirect.html',
                            {'login_url': _build_login_url(request.GET)},
                            context_instance=RequestContext(request), )
  response["P3P"] = 'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
  return response


#@login_required
def msg(request):
  try:
    limit = int(request.GET.get('limit', 10))
  except ValueError:
    limit = 10

  msgs = {
    'male': list(FbNews.objects.filter(gender=0).order_by('counter_used', 'counter_retrieved', 'last_used')[:limit/2].values('id', 'text', 'title', 'gender')),
    'female': list(FbNews.objects.filter(gender=1).order_by('counter_used', 'counter_retrieved', 'last_used')[:limit/2].values('id', 'text', 'title', 'gender'))
  }

  #FIXME: In case of high-usage the SELECT and the following UPDATE should be made with a LOCK for better gossips' usage

  # Batch update
  FbNews.objects.filter(id__in=[msg['id'] for msg in msgs['male'] + msgs['female']]).update(counter_retrieved = F('counter_retrieved') + 1)

  return HttpResponse(simplejson.dumps(msgs), mimetype='application/json')

@login_required
def publish(request):
  if util.is_param_empty('text', request.GET) or \
    util.is_param_empty('title', request.GET) or \
    util.is_param_empty('about', request.GET) or \
    util.is_param_empty('fb_id', request.GET) or \
    util.is_param_empty('msg_id', request.GET):
      return HttpResponse('ERR')

  # Find who is the news about
  about_id = _find_facebook_user(request.GET['fb_id'])
  anonymous = True if 'anonymous' in request.GET else False

  # Create the news
  news = News()
  news.user = request.user
  if about_id:
    news.about_id_id = about_id
  else:
    news.about_name = request.GET['about'].strip().title()
  news.title = request.GET['title'].strip().title()
  news.text = request.GET['text'].strip()
  news.anonymous = anonymous
  news.source = 1
  news.save();

  # Update the fb_news counter
  FbNews.objects.filter(id=request.GET['msg_id']).update(counter_used=F('counter_used') + 1, last_used=datetime.datetime.now())

  return HttpResponse(news.id)

def _find_facebook_user(fb_id):
  try:
    return Profile.objects.get(fb_id=fb_id).user_id
  except Profile.DoesNotExist:
    return None

def _login_in_main(request, fb_data):
  """
  Login to the main fingo.ro website
  """

  # FIXME: this is an ugly hack, definitely needs refactoring
  return _fb_user_to_auth(request,
                   {'uid': fb_data['user_id'],
                   'access_token': fb_data['oauth_token'],
                   'expires': fb_data['expires'],
                   })

def _build_login_url(get_dict):
  login_url = "https://www.facebook.com/login.php?"
  params = urllib.urlencode({
                            'api_key': const.FbConst.API_KEY,
                            'next': const.FULL_URL_PREFIX + "/app/",
                            'cancel_url': const.FULL_URL_PREFIX + "/",
                            'display': 'page',
                            'locale': 'ro_RO',
                            'fbconnect': 0,
                            'return_session': 0,
                            #'session_version': 3,
                            'v': '1.0',
                            'req_perms': 'email,publish_stream,user_birthday,user_hometown',
                            'canvas': 1,
                            #'legacy_return': 1
                            })
  return login_url + params



def _parse_signed_request(signed_request, secret):
  import hashlib
  import hmac
  import json
  
  l = signed_request.split('.', 2)
  encoded_sig = l[0]
  payload = l[1]

  sig = _base64_url_decode(encoded_sig)
  data = json.loads(_base64_url_decode(payload))

  if data.get('algorithm').upper() != 'HMAC-SHA256':
    log.error('Unknown algorithm')
    return None

  expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()
  if sig != expected_sig:
    return None

  return data

def _base64_url_decode(inp):
  import base64
  
  padding_factor = (4 - len(inp) % 4) % 4
  inp += "=" * padding_factor
  return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))
