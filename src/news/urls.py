from django.conf.urls.defaults import *

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('news.views',
    # Example:
    (r'^/?$', 'index', {}, 'news-index'),
    (r'^/add$', 'add', {}, 'news-add'),
    (r'^/add_inline$', 'add_inline', {}, 'news-add_inline'),
    (r'^/get$', 'get', {}, 'news-get'),
)