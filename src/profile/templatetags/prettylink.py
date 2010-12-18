from django import template
import datetime
import const

__author__="Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ ="$${date} ${time}$"


register = template.Library()

@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
url_target_blank.is_safe = True
