from django.forms.util import flatatt
from django.forms.widgets import TextInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

from profile.models import City

__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"


class CityDynamicTextInput(TextInput):
  def render(self, name, value, attrs=None):
    hidden = ''
    if value is None:
      value = ''
    final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    hidden = '<input type="hidden" name="' + final_attrs['name'] + '_hidden" id="' + final_attrs['id'] + '_hidden" value="' + unicode(value) + '"/>'
    if value != '':
      # Only add the 'value' attribute if a value is non-empty.
      city = City.objects.get(pk=value)
      final_attrs['value'] = force_unicode(self._format_value(city.name))
      
    return mark_safe(u'<input%s />%s' % (flatatt(final_attrs), hidden))

class UsersDynamicTextInput(TextInput):
  def render(self, name, value, attrs=None):
    hidden = ''
    if value is None:
      value = ''
    final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
    hidden = '<input type="hidden" name="' + final_attrs['name'] + '_hidden" id="' + final_attrs['id'] + '_hidden" value="' + unicode(value) + '"/>'
    return mark_safe(u'<input%s />%s' % (flatatt(final_attrs), hidden))

