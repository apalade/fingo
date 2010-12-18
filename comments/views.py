from comments.models import Comments
import const
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import News
from notif import NotificationSystem
from profile.templatetags import prettyuser
import util

prof = util.Prof

def index(request):
  pass

@login_required
def add(request):
  if not request.user.is_active:
    return HttpResponse('ERR')

  if request.is_ajax() or True:
    if util.is_param_empty('news_id', request.GET):
      return Http404
    if util.is_param_empty('text', request.GET):
      return HttpResponse('ERR')

    # Save new comment
    prof.start('comment-add')
    comment = Comments(user=request.user,
                       news_id=request.GET['news_id'],
                       text=request.GET['text'])
    comment.save()
    prof.stop('comment-add')

    # Send notifications
    _notify(request)
    
    return HttpResponse('OK')
  raise Http404


def get(request):
  if request.is_ajax() or True:
    if 'news_id' not in request.GET:
      raise Http404
    if 'all' not in request.GET or 'false' == request.GET['all']:
      all = False
    else:
      all = True

    prof.start('comment-get')
    comments = Comments.objects.filter(news=request.GET['news_id']).select_related('user').order_by('-time')
    comments = list(comments)
    count = len(comments)
    
    if not all:
      comments = comments[:const.NewsConst.COMMENT_DEFAULT_SHOW]
      
    comments.reverse()
    prof.stop('comment-get')

    return render_to_response('news/display_comments.html',
                              {'comments': comments,
                              'has_more': count > const.NewsConst.COMMENT_DEFAULT_SHOW and not all,
                              'news_id': request.GET['news_id']},
                              context_instance=RequestContext(request))
  raise Http404


def _notify(request):
  prof.start('comment-notify')
  comments = Comments.objects.filter(news=request.GET['news_id']).exclude(user=request.user)
  # Notify all the people we need to
  news = News.objects.filter(id=request.GET['news_id']).select_related('user', 'about_id')
  for n in news:
    # Should be only one actually
    if n.user != request.user:
      comments = comments.exclude(user=n.user)
      NotificationSystem.create(n.user, const.NotifConst.NEW_COMMENT_GOSSIP_MINE,
                                {'username': request.user.username,
                                'name': prettyuser.user_or_first_name(request.user),
                                'news_id': request.GET['news_id'],
                                })
    elif n.about_id and n.about_id != request.user:
      comments = comments.exclude(user=n.about_id)
      NotificationSystem.create(n.about_id, const.NotifConst.NEW_COMMENT_GOSSIP_ME,
                                {'username': request.user.username,
                                'name': prettyuser.user_or_first_name(request.user),
                                'news_id': request.GET['news_id'],
                                })
  participants = User.objects.filter(id__in=comments.distinct().values('user'))
  for participant in participants:
    NotificationSystem.create(participant, const.NotifConst.NEW_COMMENT_GOSSIP,
                              {'username': request.user.username,
                              'name': prettyuser.user_or_first_name(request.user),
                              'news_id': request.GET['news_id'],
                              })
  prof.stop('comment-notify')