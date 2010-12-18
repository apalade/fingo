from django.conf.urls.defaults import *

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('fb_app.views',
    # Example:
    (r'^/?$', 'index', {}, 'fb_app-index'),
    (r'^/msg$', 'msg', {}, 'fb_app-msg'),
    (r'^/publish$', 'publish', {}, 'fb_app-publish'),
)