from comments.models import Comments
import const
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import facebook
from fingo_new.notif import NotificationSystem
from friends.models import Friends
from news.forms import AddNewsForm
from news.forms import AddNewsInlineForm
from news.models import Image
from news.models import News
from notif import FacebookSystem
from notif import NotificationSystem
from profile.models import Profile
from profile.templatetags import prettyuser
import util

prof = util.Prof

def index(request):
  prof.start('12-users-left')
  profile = request.user.get_profile() if request.user.is_authenticated() else None
  latest_users_profiles = list(Profile.objects.order_by('-user__date_joined').select_related(depth=1)[:6])
  best_news = News.objects.filter(about_id__isnull=False).values('about_id').annotate(num_news=Count('about_id')).order_by('-num_news')[:6]
  best_users_profiles = list(Profile.objects.filter(user__in=[news['about_id'] for news in best_news]).select_related(depth=1))
  prof.stop('12-users-left')
    
  form_add_news = AddNewsInlineForm()
  return render_to_response('news/index.html',
                            {'profile': profile,
                            'app_url': const.FbConst.APP_URL,
                            'add_news_about': True,
                            'form_add_news': form_add_news,
                            'latest_users_profiles': latest_users_profiles,
                            'best_users_profiles': best_users_profiles,
                            'curr_page': 'news-index',
                            'js': ('news.js', 'jquery-multifile.js', 'jquery-form.js', 'jquery-ui.js'),
                            'css': ('ui/ui.css',), },
                            context_instance=RequestContext(request))


def _add(request, form):
  # Check if the user is active or not
  if not request.user.is_active:
    return

  # Save news
  prof.start('news-add')
  news = form.save(commit=False)
  news.user = request.user
  news.save()
  prof.stop('news-add')

  # Publish on wall?
  if not('anonymous' in form.cleaned_data and form.cleaned_data['anonymous']):
    if 'fb_wall' in form.cleaned_data and form.cleaned_data['fb_wall']:
        try:
          FacebookSystem.post_gossip_to_wall(request.COOKIES,
                                             news,
                                             'me')
        except facebook.GraphAPIError:
          # TODO: Error when the user logs out from facebook between
          # loading /news/add and submiting it
          pass

  # Save images if any
  prof.start('news-add-save-images')
  for image in request.FILES.getlist('images'):
    img = Image(news=news, image=image)
    img.save()
  prof.stop('news-add-save-images')


  # Send e-mail
  if news.about_id:
    NotificationSystem.create(news.about_id, 
                              const.NotifConst.NEW_GOSSIP_ME,
                              {'username': request.user.username,
                              'anonymous': news.anonymous,
                              'name': prettyuser.user_or_first_name(request.user),
                              })

@login_required
def add(request):
  if request.method == 'POST':
    if request.POST['about_name_hidden'] != '' and request.POST['about_name'] != '':
      request.POST['about_id'] = request.POST['about_name_hidden']
      request.POST['about_name'] = ''

    form = AddNewsForm(request.POST, request.FILES)
    if form.is_valid():
      _add(request, form)
      return HttpResponseRedirect('/')
  else:
    form = AddNewsForm(initial={'fb_wall': True, 'video': 'http://'})

  return render_to_response('news/add.html',
                            {'form': form,
                            'js': ('jquery-ui.js', 'jquery-multifile.js'),
                            'css': ('ui/ui.css',)},
                            context_instance=RequestContext(request))

@login_required
def add_inline(request):
  if request.is_ajax() or True:
    if request.POST['about_id'] == '' and request.POST['about_name'] == '':
      return HttpResponse('ERR')
    
    form = AddNewsInlineForm(request.POST, request.FILES)
    if form.is_valid():
      for image in request.FILES.getlist('images'):
        if image.size > const.FormConst.News.MAX_IMAGE_SIZE:
          returnHttpResponse('ERR')
      _add(request, form)
      return HttpResponse("OK")
    else:
      return HttpResponse('ERR')
  raise Http404

def get(request):
  if request.is_ajax() or True:
    has_more = False
    
    (page, perpage, filter, cityId, countyId, comments, exclude, about) = _get_defaults(request, request.GET)
    offset = (int(page) - 1) * perpage
    if offset < 0:
      offset = 0

    if about == -1:
      about = request.user.id

    prof.start('news-get')
    news = News.objects
    if exclude != -1:
      news = news.exclude(pk=exclude)
    if filter == const.NewsConst.Filter.ALL:
      pass
    elif filter == const.NewsConst.Filter.FRIENDS:
      if request.user.is_authenticated():
        friendIds = Friends.objects.filter(user=request.user,
                                           accepted=True).values('friend')
        news = news.filter(about_id__in=friendIds)
    elif filter == const.NewsConst.Filter.CITY and cityId is not None:
      city_mixup = Q(about_id__profile__city_curr=cityId) | Q(about_id__profile__city_home=cityId)
      news = news.filter(about_id__isnull=False).filter(city_mixup)
    elif filter == const.NewsConst.Filter.COUNTY and countyId is not None:
      county_mixup = Q(about_id__profile__city_curr__county__id=countyId) | \
        Q(about_id__profile__city_home__county__id=countyId)
      news = news.filter(about_id__isnull=False).filter(county_mixup)
    elif filter == const.NewsConst.Filter.PHOTO:
      news = news.filter(id__in=Image.objects.values('news').distinct())
    elif filter == const.NewsConst.Filter.VIDEO:
      news = news.exclude(video='')
    elif filter == const.NewsConst.Filter.ABOUT:
      news = news.filter(about_id__isnull=False).filter(about_id=about)

    # Fetch news
    if news.count() > offset + perpage:
      has_more = True
    news = news.order_by('-time').select_related('user', 'about_id')[offset: offset + perpage]

    # Finally, fetch images, comments count for the news objects
    # TODO: improve SQL here - too many hits in the database
    for n in news:
      n.images = Image.objects.filter(news=n).order_by('id')
      if not comments:
        n.comments_count = Comments.objects.filter(news=n).count()
    list(news)
    prof.stop('news-get')
    
    return render_to_response('news/display_news.html',
                              {'news': news, 'has_more': has_more, 'app_url': const.FbConst.APP_URL},
                              context_instance=RequestContext(request))
  raise Http404


def _get_defaults(request, params):
  # Do not allow clients to retrieve all the news at once
  perpage = int(params.get('perpage', const.NewsConst.NEWS_PER_PAGE))
  if perpage > const.NewsConst.NEWS_PER_PAGE:
    perpage = const.NewsConst.NEWS_PER_PAGE

  return (int(params.get('page', 1)),
          perpage,
          int(params.get('filter', const.NewsConst.Filter.ALL)),
          params.get('cityId', None),
          params.get('countyId', None),
          True if params.get('comments', 'true') == 'true' else False,
          params.get('exclude', -1),
          params.get('about', request.user.id)
          )