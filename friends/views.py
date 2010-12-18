import itertools

import const
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from friends.forms import InviteFormCredentials
from friends.forms import InviteFormPeople
from friends.models import Friends
from news.forms import AddNewsInlineForm
from notif import InviteSystem
from notif import NotificationSystem
from profile.templatetags import prettyuser
import util

prof = util.Prof

@login_required
def index(request):
  if 'p' in request.GET:
    try:
      user_id = int(request.GET['p'])
    except ValueError:
      raise Http404
    else:
      try:
        user = User.objects.get(pk = user_id)
      except User.DoesNotExist:
        raise Http404
    friendships = None
  else:
    user = request.user
    # Displaying the waiting friendships...
    NotificationSystem.receipt(request.user, const.NotifConst.FRIEND_REQ)
    friendships = Friends.objects.filter(Q(friend=request.user)).\
      filter(accepted=False).filter(ignored=False)

  prof.start('profile-stats')
  total_friends = Friends.objects.filter(Q(friend=user) | Q(user=user)).filter(accepted=True).count()
  total_women = Friends.objects.filter(friend=user).filter(accepted=True).filter(user__profile__gender=1).count() + \
    Friends.objects.filter(user=user).filter(accepted=True).filter(friend__profile__gender=1).count()
  total_waiting = Friends.objects.filter(Q(friend=user) | Q(user=user)).filter(accepted=False).filter(ignored=False).count()
  total_ignored = Friends.objects.filter(Q(friend=user) | Q(user=user)).filter(ignored=True).count()
  prof.stop('profile-stats')
  
  return render_to_response('friends/index.html',
                            {'js': ('friends.js', 'news.js',
                              'jquery-multifile.js', 'jquery-ui.js',
                              'jquery-form.js'),
                              'css': ('ui/ui.css',),
                            'curr_page': 'friends-index',
                            'stats': {'total': total_friends,
                                      'women': total_women,
                                      'men': total_friends - total_women,
                                      'waiting': total_waiting,
                                      'ignored': total_ignored},
                            'req_user': user,
                            'form_add_news': AddNewsInlineForm(),
                            'friendships': friendships},
                            context_instance=RequestContext(request))


@login_required
def get(request):
  if request.is_ajax() or True:
    (page, perpage, term, user_id) = _get_defaults(request.GET)
    offset = (int(page) - 1) * perpage
    if offset < 0:
      offset = 0

    try:
      user_id = int(user_id)
    except ValueError:
      user = request.user
    else:
      try:
        user = User.objects.get(pk=user_id)
      except User.DoesNotExist:
        user = request.user

    friendships1 = Friends.objects.filter(Q(user=user)).filter(accepted=True).values_list('friend')
    friendships2 = Friends.objects.filter(Q(friend=user)).filter(accepted=True).values_list('user')
    
    friends = User.objects.filter(pk__in=(x[0] for x in itertools.chain(friendships1, friendships2)))
    friends = util.get_matching_users(friends, term);

    count = len(friends)
    friends = friends[offset:offset + perpage]
    return render_to_response('friends/display.html',
                              {'friends': friends,
                              'has_next': count > offset + perpage,
                              'has_prev': offset > 0,
                              'js': ('friends.js', )},
                              context_instance=RequestContext(request))

@login_required
def add(request):
  if request.is_ajax() or True:
    try:
      friend = User.objects.get(pk=request.GET['id'])
    except User.DoesNotExist:
      raise Http404

    try:
      Friends.objects.get(Q(user=request.user, friend=friend) | Q(user=friend, friend=request.user))
    except Friends.DoesNotExist:
      # Save new request
      f = Friends(user=request.user, friend=friend)
      f.save()

      # Send notification
      NotificationSystem.create(friend, const.NotifConst.FRIEND_REQ)
      
      return HttpResponse('OK')
    else:
      return HttpResponse('ERR')
    

@login_required
def confirm(request):
  if request.is_ajax() or True:
    if not('confirm' in request.GET and 'id' in request.GET):
      raise Http404

    try:
      friend = User.objects.get(pk=request.GET['id'])
    except User.DoesNotExist:
      raise Http404

    try:
      friendship = Friends.objects.get(user=friend, friend=request.user)
      if friendship.accepted or friendship.ignored:
        return HttpResponse('ERR')

      if request.GET['confirm'] == 'accept':
        friendship.accepted = True
        friendship.ignored = False
        friendship.email_sent = True

        # Send an e-mail
        NotificationSystem.create(friend, const.NotifConst.FRIEND_CONFIRM, {'username': friend.username, 'name': prettyuser.user_or_first_name(friend)})
      else:
        friendship.accepted = False
        friendship.ignored = True
        friendship.email_sent = True

      friendship.save()
    except Friends.DoesNotExist:
      raise Http404

    return HttpResponse('OK')

@login_required
def invite(request):
  wrong = False
  
  if request.method == 'POST':
    if 'send' in request.GET:
      # final step, actually send e-mails
      form_people = InviteFormPeople(request.POST)
      for email in request.POST.getlist('people'):
        InviteSystem.invite(email, 
                            {'username': request.user.username,
                            'name': prettyuser.user_or_first_name(request.user),
                            'email': email
                            })
      return HttpResponseRedirect('/friends')
    else:
      # get contacts and make him choose
      form_cred = InviteFormCredentials(request.POST)
      if form_cred.is_valid():
        contacts = InviteSystem.getContacts(form_cred.cleaned_data['username'],
                                            form_cred.cleaned_data['password'],
                                            form_cred.cleaned_data['type'])
        if contacts is None:
          # wrong credentials
          wrong = True
          step = 0
        else:
          form_people = InviteFormPeople(choices=contacts)
          step = 1;
      else:
        step = 0;
  else:
    form_cred = InviteFormCredentials()
    step = 0;

  return render_to_response('friends/invite.html',
                            {'step': step,
                            'wrong': wrong,
                            'form': form_cred if 0 == step else form_people, },
                            context_instance=RequestContext(request))



def _get_defaults(params):
  return (int(params.get('page', 1)),
          int(params.get('perpage', const.FriendsConst.FRIENDS_LIST_PER_PAGE)),
          params.get('term', ''),
          params.get('user_id', 'NOUSER'))