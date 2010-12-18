from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', 'news.views.index'),
    (r'^app', include('fingo_new.fb_app.urls')),
    (r'^profile', include('fingo_new.profile.urls')),
    (r'^news', include('fingo_new.news.urls')),
    (r'^friends', include('fingo_new.friends.urls')),
    (r'^comments', include('fingo_new.comments.urls')),
    (r'^message', include('fingo_new.message.urls')),
    (r'^notif', include('fingo_new.notif.urls')),
    (r'^about$', 'blah.views.about'),
    (r'^terms$', 'blah.views.terms'),
    (r'^(?P<username>[A-Za-z0-9\._-]+)$', 'profile.views.profile', {} , 'profile-view'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs'
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
