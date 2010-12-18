from django import template
import datetime
import const

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"


register = template.Library()

@register.filter
def default_time(complete_date):
  diff = datetime.datetime.now() - complete_date
  if diff.days < 1:
    if diff.seconds < 60:
      return const.NewsConst.Time.SOME_SECONDS

    minutes = diff.seconds / 60.
    if minutes < 10:
      return const.NewsConst.Time.SOME_MINUTES
    if minutes < 40:
      return const.NewsConst.Time.HALF_AN_HOUR

    hours = minutes / 60.
    if hours < 1:
      return const.NewsConst.Time.ALMOST_AN_HOUR
    if hours < 2:
      return const.NewsConst.Time.AN_HOUR
    if hours < 24:
      return const.NewsConst.Time.SOME_HOURS % round(hours)

  d = complete_date.date()
  t = complete_date.time()
  return  '%d.%d.%d %d:%d' % (d.day, d.month, d.year, t.hour, t.minute)

@register.filter
def pretty_bday(bday):
  if bday is None:
    return

  import locale
  locale.setlocale(locale.LC_ALL, ('ro_RO', 'UTF8'))
  if 1900 == bday.year:
    pretty = bday.strftime("%d %B")
  else:
    pretty = bday.strftime("%d %B %Y")
  locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())

  return pretty


  


