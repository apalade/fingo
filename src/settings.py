# Django settings for fingo_new project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
          ('Alexandru Palade', 'alexandru.palade@loopback.ro'),
          )

MANAGERS = ADMINS

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': 'fingo', # Or path to database file if using sqlite3.
    'USER': 'fingo', # Not used with sqlite3.
    'PASSWORD': '12345', # Not used with sqlite3.
    'HOST': 'localhost', # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '', # Set to empty string for default. Not used with sqlite3.
  }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'vw},up%pDv5!'
EMAIL_HOST_USER = 'alerte@fingo.ro'
EMAIL_USE_TLS = True


# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Bucharest'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://192.168.212.1/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '=ivg$6tb7oy@t4o6sj4d5zm#g!qi$-2=$2vym!x6^yg=gm(8#5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    #     'django.template.loaders.eggs.Loader',
                    )

MIDDLEWARE_CLASSES = (
                      'django.middleware.common.CommonMiddleware',
                      'django.contrib.sessions.middleware.SessionMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware',
                      'django.contrib.auth.middleware.AuthenticationMiddleware',
                      'django.contrib.messages.middleware.MessageMiddleware',
		      'debug_toolbar.middleware.DebugToolbarMiddleware',
                      )

ROOT_URLCONF = 'fingo_new.urls'

TEMPLATE_DIRS = (
                 "/static/templates/"
                 # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
                 # Always use forward slashes, even on Windows.
                 # Don't forget to use absolute paths, not relative paths.
                 )

INSTALLED_APPS = (
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.sites',
                  'django.contrib.messages',
                  # Uncomment the next line to enable the admin:
                  'django.contrib.admin',
                  'fingo_new.message',
                  'fingo_new.news',
                  'fingo_new.comments',
                  'fingo_new.profile',
                  'fingo_new.friends',
                  'fingo_new.notif',
                  'fingo_new.debug_toolbar',
                  'fingo_new.fb_app',

                  )
def custom_show_toolbar(request):
    return 'debugme' in request.COOKIES

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
}

# Not default
AUTH_PROFILE_MODULE = "profile.Profile"
LOGIN_URL = '/profile/login'
TEMPLATE_CONTEXT_PROCESSORS = (
                               "django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.contrib.messages.context_processors.messages",
                               'fingo_new.context.notifications',
                               'fingo_new.context.fb_app_id',
                               'fingo_new.context.news_scroll'
                               )
PROFILING = True
