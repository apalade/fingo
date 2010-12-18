 # -*- coding: utf-8 -*-
import volatile

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"

FULL_URL_PREFIX = volatile.FULL_URL_PREFIX
MSG_SUBJECT_MAX_LENGTH = 1024
CITY_MAX_LENGTH = 50


class NotifConst:
  NONE = 0
  MSG = 1
  FRIEND_REQ = 1 << 1
  FRIEND_CONFIRM = 1 << 2
  FRIEND_SUGG = 1 << 3
  NEW_COMMENT_GOSSIP = 1 << 4
  NEW_COMMENT_GOSSIP_ME = 1 << 5
  NEW_COMMENT_GOSSIP_MINE = 1 << 6
  NEW_GOSSIP_ME = 1 << 7
  INVITE = 1 << 8

  # Email settings
  BULK_AT_ONCE = 10
  SUBJECT = {
    MSG: u'Mesaj nou pe fingo.ro',
    FRIEND_REQ: u'Cineva vrea să te cunoască',
    FRIEND_CONFIRM: u'Confirmare prietenie',
    FRIEND_SUGG: u'Sugestie prieten',
    NEW_COMMENT_GOSSIP: u'Un nou comentariu la o bârfă pe care o urmărești',
    NEW_COMMENT_GOSSIP_ME: u'Un nou comentariu la o bârfă despre tine',
    NEW_COMMENT_GOSSIP_MINE: u'Un nou comentariu la o bârfă scrisă de tine',
    NEW_GOSSIP_ME: u'Cineva te-a bârfit',
    INVITE: u'Bârfă caldă'
  }
  FROM = 'Alerte Fingo <alerte@fingo.ro>'
  NO_REPLY = 'no-reply@fingo.ro'

  # Inviter settings
  class Inviter:
    PHP_PATH = volatile.PHP_PATH
    PHP_ARGS = '-q'
    PATH = volatile.INVITER_PATH


class NewsConst:
  COMMENT_MAX_LENGTH = 1024
  COMMENT_DEFAULT_SHOW = 3
  LINK_MAX_LENGTH = 1024
  ABOUT_NAME_MAX_LENGTH = 128
  TITLE_MAX_LENGTH = 255
  NEWS_PER_PAGE = 6

  class Scroll:
    NEW_USER = u"<a href=\"%s\">%s</a> s-a înregistrat pe Fingo.ro"
    NEW_USER_MAX = 3
    NEW_GOSSIP = u"<a href=\"%s\">%s</a> a bârfit despre <a href=\"%s\">%s</a> (<a href=\"%s\">%s</a>)"
    NEW_GOSSIP_ANONYMOUS = u"S-a bârfit despre <a href=\"%s\">%s</a> (<a href=\"%s\">%s</a>)"
    NEW_GOSSIP_MAX = 4
    NEW_FRIEND = u"<a href=\"%s\">%s</a> este prieten cu <a href=\"%s\">%s</a>"
    NEW_FRIEND_MAX = 3

  class Filter:
    ALL = 0
    FRIENDS = 1
    CITY = 2
    COUNTY = 4
    PHOTO = 8
    VIDEO = 16
    ABOUT = 32

  class Time:
    SOME_SECONDS = "acum câteva secunde"
    SOME_MINUTES = "acum câteva minute"
    HALF_AN_HOUR = "acum o jumătate de oră"
    ALMOST_AN_HOUR = "acum aproape o oră"
    AN_HOUR = "acum o oră"
    SOME_HOURS = "acum %d ore"

class FbConst:
  APP_ID = volatile.FB_APP_ID
  APP_SECRET = volatile.FB_APP_SECRET
  API_KEY = volatile.FB_API_KEY
  APP_URL = volatile.FB_APP_URL
  WALL_MSG_LENGTH = 100

class FriendsConst:
  FRIENDS_LIST_PER_PAGE = 12
  PROFILE_FRIENDS = 9
  
class FormConst:
  REQUIRED = u"Acest câmp este necesar"
  EMAIL_MAX_LENGTH = 255
  
  class Register:
    USERNAME = u"Utilizator"
    PASSWORD = u"Parolă"
    PASSWORD2 = u"Confirmă parolă"
    EMAIL = u"Adresă de e-mail"
    FIRST_NAME = u"Prenume"
    LAST_NAME = u"Nume"

    DIFFERENT = u"Parolele nu coincid"
    UNIQUE = u"Avem înregistrată această valoare deja în baza de date"
    TOO_SHORT = u"Parolă prea scurtă"

  class Profile:
    GENDER = u"Genul"
    BDAY = u"Ziua de naștere"
    CITY_CURR = u"Orașul curent"
    CITY_HOME = u"Orașul natal"
    PHOTO = u"Poză"

  class News:
    ANONYMOUS = u"Nu arăta cine sunt"
    ABOUT_NAME = u"Despre"
    TITLE = u"Titlul bârfei tale"
    TEXT = u"Ce vrei să ne zici"
    IMAGE = u"Adaugă și o imagine dacă ai"
    VIDEO = u"Adaugă și un video dacă ai"
    FB_WALL = u"Adaugă și pe Facebook"

    # Add inline
    MAX_IMAGE_SIZE = 3145728            # 3MB
    ERR_TITLE_REQUIRED = 'Nu ai completat titlul'
    ERR_TEXT_REQUIRED = 'Nu ai completat continutul barfei'
    ERR_PHOTO_SIZE = 'Fiecare poză nu trebuie sa fie mai mare de 2.5MB'
    ERR_VIDEO = 'Link-ul catre video nu este bun'

  class Invite:
    USERNAME = u"E-mail"
    PASSWORD = u"Parolă"
    PEOPLE = u"Alege din persoane"
    DOMAIN_REGEX_YAHOO = "yahoo.*"
    DOMAIN_REGEX_GMAIL = "gmail\.com|googlemail\.com"
    DOMAIN_SUPPORT = u"Ne pare rău, dar nu suportăm decât Yahoo! și Gmail momentan."

class LogConst:
  CONFIG = volatile.LOG_CONFIG
  ROTATE_AT = 'midnight'


if __name__ == "__main__":
    pass
