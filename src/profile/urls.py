from django.conf.urls.defaults import *

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('profile.views',
    # Example:
    (r'^/?$', 'index', {}, 'profile-index'),
    (r'^/update$', 'update', {} , 'profile-update'),
    (r'^/login$', 'login', {}, 'profile-login'),
    (r'^/logout$', 'logout', {}, 'profile-logout'),
    (r'^/city$', 'city', {}, 'profile-city'),
    (r'^/users$', 'users', {}, 'profile-users'),
)