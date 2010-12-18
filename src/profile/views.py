# -*- coding: utf-8 -*-

import json
import time

import const
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import uploadedfile
from django.db import transaction, connection
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import facebook
from friends.models import Friends
from news.forms import AddNewsInlineForm
from news.models import Image
from news.models import News
from notif import FacebookSystem
from notif import NotificationSystem
from profile.forms import ProfileForm
from profile.models import City
from profile.models import Profile
import random
import string
import util

prof = util.Prof
log = util.log

#@login_required
def index(request):
  req_news = False
  if 'n' in request.GET:
    try:
      int(request.GET['n'])
    except ValueError:
      pass
    else:
      try:
        req_news = News.objects.get(id=request.GET['n'].strip())
        req_news.images = Image.objects.filter(news=req_news)
      except News.DoesNotExist:
        pass
      else:
        if 'facebookexternalhit' in request.META['HTTP_USER_AGENT']:
          return render_to_response('profile/for_facebook.html',
                                    {'req_news': req_news},
                                    context_instance=RequestContext(request))
  if request.user.is_authenticated():
    form_add_news = AddNewsInlineForm()
    profile = request.user.get_profile()
    NotificationSystem.receipt(request.user, const.NotifConst.NEW_GOSSIP_ME)
    return render_to_response('profile/index.html',
                              {'profile': profile,
                              'app_url': const.FbConst.APP_URL,
                              'curr_page': 'profile-index',
                              'add_news_about': True,
                              'form_add_news': form_add_news,
                              'js': ('news.js',
                              'jquery-multifile.js', 'jquery-ui.js',
                              'jquery-form.js'),
                              'css': ('ui/ui.css', ),
                              'req_news': req_news, },
                              context_instance=RequestContext(request))
  else:
    redirect_to = '/profile/login?next=/profile'
    if req_news:
      redirect_to += '?n=' + request.GET['n']
    return HttpResponseRedirect(redirect_to)

@login_required
def profile(request, username=None):
  curr_page = False
  if username == None:
    return HttpResponseRedirect('/profile')
  else:
    if username == request.user.username:
      curr_page = 'profile-view'
    user = util.get_user(username)

  if user is None:
    raise Http404

  # Are we friends?
  prof.start('profile-check-friend')
  count = Friends.objects.filter(Q(user=request.user, friend=user) | Q(user=user, friend=request.user)).count()
  if count > 0:
    is_my_friend = True
  else:
    is_my_friend = False
  prof.stop('profile-check-friend')

  # Discover all accepted friends
  prof.start('profile-accepted-friends')
  friends_count = Friends.objects.filter(Q(friend=user) | Q(user=user)).filter(accepted=True).count()
  friends = Friends.objects.filter(Q(friend=user) | Q(user=user)).filter(accepted=True).values('user', 'friend')[:const.FriendsConst.PROFILE_FRIENDS]
  ids = []
  for friend in [friend.values() for friend in friends]:
    if friend[0] != user.id:
      ids.append(friend[0])
    if friend[1] != user.id:
      ids.append(friend[1])
  friends_profiles = list(Profile.objects.filter(user__in=ids).select_related(depth=1))
  prof.stop('profile-accepted-friends')

  # Build forms
  form_add_news = AddNewsInlineForm(initial={'about_id': user.id, 'video': 'http://'})
  form_profile = ProfileForm(initial={'first_name': request.user.first_name,
                             'last_name': request.user.last_name},
                             instance=user.get_profile())

  return render_to_response('profile/profile.html',
                            {'req_user': user,
                            'add_news_about_name_hide': True,
                            'form_add_news': form_add_news,
                            'form_profile': form_profile,
                            'curr_page': curr_page,
                            'is_my_friend': is_my_friend,
                            'friends_count': friends_count,
                            'friends_profiles': friends_profiles,
                            'js': ('profile.js', 'news.js',
                            'jquery-multifile.js', 'jquery-form.js', 'jquery-ui.js'),
                            'css': ('ui/ui.css', )},
                            context_instance=RequestContext(request))


  


@login_required
def update(request):
  if request.is_ajax() or True:
    data = request.GET
    profile = request.user.get_profile()

    if 'city_curr' in data and data['city_curr'] != '':
      profile.city_curr_id = data['city_curr_hidden']
    elif 'city_home' in data and data['city_home'] != '':
      profile.city_home_id = data['city_home_hidden']
    elif 'first_name' in data and data['first_name'] != '':
      profile.first_name = data['first_name']
    elif 'last_name' in data and data['last_name'] != '':
      profile.last_name = data['last_name']
    elif 'gender' in data and data['gender'] != '':
      profile.gender = data['gender']
    elif 'bday' in data and data['bday'] != '':
      profile.bday = data['bday']
    profile.save()

    # Save name
    if 'first_name' in data and data['first_name'] != '':
      request.user.first_name = data['first_name'].strip()
    elif 'last_name' in data and data['last_name'] != '':
      request.user.last_name = data['last_name'].strip()
    request.user.save()

    # Redirect to profile
    return HttpResponse('OK')
  return HttpResponse('ERR')

  
def login(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/')

  if 'next' in request.GET and request.GET['next'] != '':
    next = request.GET['next']
  else:
    next = '/profile/'

  fb_user = facebook.get_user_from_cookie(request.COOKIES, 
                                          const.FbConst.APP_ID,
                                          const.FbConst.APP_SECRET)
  print fb_user
  if fb_user is not None:
    # Expire the session along with the facebook's one
    expire_at = datetime.datetime.fromtimestamp(float(fb_user['expires']))
    request.session.set_expiry(expire_at)

    # Login with the facebook account (and save new data)
    user = _fb_user_to_auth(request, fb_user)
    if user is None:
      # F*cked up facebook session, clear it and retry
      response = HttpResponseRedirect('/profile/login')
      response.delete_cookie('fbs_' + const.FbConst.APP_ID)
      return response

    
    # Ugly hack here to login in our system - what to do?
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    auth.login(request, user)

    # Redirect
    return HttpResponseRedirect(next);

  return render_to_response('profile/login.html',
                            {'next': next, },
                            context_instance=RequestContext(request))

def logout(request):
  """
  Logouts users from our system
  """
  auth.logout(request)
  return HttpResponseRedirect('/')
                            
@login_required
def city(request):
  """
  Ajax Request to search for cities
  """
  if 'term' not in request.GET:
    raise Http404
  
  if request.is_ajax():
    cities_list = []
    cities = City.objects.filter(name__icontains=request.GET['term']).order_by('type')
    for city in cities:
      cities_list.append({'id': city.id, 
                         'label': city.name + ' (' + city.county.name + ')',
                         'value': city.name})
    return HttpResponse(json.dumps(cities_list), mimetype='application/javascript')



@login_required
def users(request):
  """
  Ajax Request to search for user after first, last name and username
  """
  if 'term' not in request.GET:
    raise Http404
  
  if request.is_ajax() or True:
    users_list = []

    prof.start('profile-get-users-ajax')
    users = util.get_matching_users(User.objects, request.GET['term'])
    for user in users:
      if user.first_name != '' or user.last_name != '':
        name = user.first_name + ' ' + user.last_name + ' (' + user.username + ')'
      else:
        name = user.username
      users_list.append({'id': user.id,
                        'label': name,
                        'value': name})
    prof.stop('profile-get-users-ajax')
    return HttpResponse(json.dumps(users_list), mimetype='application/javascript')


def _fb_user_to_auth(request, fb_user_cookie):
  prof.start('profile-save-fb-get-me')
  graph = facebook.GraphAPI(access_token=fb_user_cookie['access_token'])
  try:
    fb_user = graph.get_object("me")
  except facebook.GraphAPIError:
    # Clear cookies
    return None
  prof.stop('profile-save-fb-get-me')

  log.debug("fb_user_cookie %s fb_user_me: %s" % (str(fb_user_cookie), str(fb_user)))
  prof.start('profile-save-fb-new-user')
  (user, profile, new_user) = _check_and_save_user_atomic(fb_user)
  prof.stop('profile-save-fb-new-user')
  if new_user:
    # A new user, we also need to save to profile
    fb_user['photo'] = graph.request("me/picture", args={'type': 'large'}, binary=True)
    _populate_user_profile(user, profile, fb_user, fb_user_cookie)

    # Make friends in facebook for fingo too
    _save_friends(user, graph.get_connections("me", "friends")['data'])

    # Post it to wall
    # FIXME: this will fail if it comes from fb_app
    FacebookSystem.post_new_user_to_wall(request.COOKIES)

  return user

@transaction.commit_on_success
@util.require_lock(User, 'ACCESS EXCLUSIVE')
def _check_and_save_user_atomic(fb_user):
  try:
    #FIXME: This can be improved to be checked after uid in the facebook cookie
    user = User.objects.get(email=fb_user['email'])
    return (user, None, False)

  except User.DoesNotExist:
    # Save it to our db
    username = _get_username_from_fb_user(fb_user)
    user = User.objects.create(username=username, email=fb_user['email'],
          first_name=fb_user['first_name'].title(),
          last_name = fb_user['last_name'].title())
    profile = Profile()
    profile.user = user
    profile.save(force_insert=True)
    
    return (user, profile, True)

def _populate_user_profile(user, profile, fb_user, fb_user_cookie):
  prof.start('profile-save-fb-new-user-profile')
  
  if 'birthday' in fb_user:
    try:
      profile.bday = time.strftime("%Y-%m-%d",
                                   time.strptime(fb_user['birthday'], "%m/%d/%Y"))
    except ValueError:
      profile.bday = time.strftime("%Y-%m-%d",
                                   time.strptime(fb_user['birthday'], "%m/%d"))

  if 'gender' in fb_user:
    if fb_user['gender'].lower() == 'female' or fb_user['gender'].lower() == 'feminin' or fb_user['gender'].lower() == 'femeie':
      profile.gender = 1
    else:
      profile.gender = 0

  profile.fb_id = fb_user_cookie['uid']
  try:
    profile.city_curr = _get_city(fb_user['location']['name'])
    profile.city_home = _get_city(fb_user['hometown']['name'])
  except:
    # Just couldn't get the city, that's all
    pass
  
  profile.photo = uploadedfile.SimpleUploadedFile(_parse_last_part_link(fb_user['photo']['link']),
                                                  fb_user['photo']['contents'])
  profile.save(force_update=True)
  
  if profile.city_curr is None or profile.city_home is None:
    # Delete photo
    fb_user['photo'] = None
    util.log.warning("Current/Home city detection failure " + str(fb_user))

  prof.stop('profile-save-fb-new-user-profile')
  
  return user

def _save_friends(user, friends):
  # No friends, no glory
  if len(friends) < 1:
    return

  prof.start('profile-save-fb-friends')
  ids = []
  for friend in friends:
    ids.append(friend['id'])
  user_ids = Profile.objects.filter(fb_id__in=ids).values('user')

  # No common friends, no glory
  if len(user_ids) < 1:
    return

  # Bulk insert friends from facebook
  query = "INSERT INTO friends_friends (user_id, friend_id, accepted, ignored, added_on, modified_on) VALUES ";
  for user_id in user_ids:
    query += "(%d, %d, true, false, NOW(), NOW())," % (user.id, user_id['user'])
  connection.cursor().execute(query[:-1])
  transaction.commit_unless_managed()
  prof.stop('profile-save-fb-friends')


def _get_username_from_fb_user(fb_user):
  """
  Either from link or first letter from first name and the whole lastname
  """
  link = fb_user.get('link', '')
  username = _parse_last_part_link(link)
  if '?' in username:
    username = _generate_username(fb_user)

  return username.replace(' ', '_')

def _parse_last_part_link(link):
  return link.rsplit('/', 1)[1]

def _generate_username(fb_user):
  first = fb_user['first_name'].replace(' ', '_').replace('-', '_')
  last = fb_user['last_name'].replace(' ', '_').replace(' ', '_')

  if first == '':
    first = 'x'
  if last == '':
    last = 'x'

  usernames = (first[0] + last,
               first + '.' + last,
               first + last,
               first + '_' + last,

               last[0] + first,
               last + '.' + first,
               last + first,
               last + '_' + first,

               fb_user['email'].split('@')[0],

               first[0] + last + str(random.randint(0, 9999)),
               first + '.' + last + str(random.randint(0, 9999)),
               first + last + str(random.randint(0, 9999)),
               first + '_' + last + str(random.randint(0, 9999)))


  for username in usernames:
    try:
      username = username.decode('ascii')
    except UnicodeEncodeError:
      continue

    username = username.strip().lower()
    if username == '':
      continue
      
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username

  # This should be fucking incredible :)
  return ''.join([random.choice(string.letters + string.digits) for i in range(7)])

def _get_city(name):
  city = None
  county = None
  country = None

  try:
    (city, county, country) = map(unicode.strip, name.split(','))
  except ValueError:
    try:
      (city, country) = map(unicode.strip, name.split(','))
    except ValueError:
      city = name.strip()

  # If not Romania we are not interested
  if country is not None and country.lower() != u'romania' and country.lower() != u'românia':
    return None

  # Special hack here for Bucharest
  if city.lower() == u'bucharest' or city.lower() == u'bucure\u015fti':
    city = u'Bucuresti'

  # See how many do we match
  cities = City.objects.filter(name__iexact=city)
  if len(cities) < 1:
    return None
  elif len(cities) > 1 and county is not None:
    for c in cities:
      if c.county.name.lower() == county.lower():
        return c
  return cities[0]
