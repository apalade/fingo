from django.conf.urls.defaults import *

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('comments.views',
    # Example:
    (r'^/?$', 'index'),
    (r'^/add$', 'add'),
    (r'^/get$', 'get'),
)