from django import forms
import re

from const import FormConst

__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"

class InviteFormCredentials(forms.Form):
  username = forms.EmailField(label=FormConst.Invite.USERNAME)
  password = forms.CharField(label=FormConst.Invite.PASSWORD,
                             widget=forms.PasswordInput, min_length=1)

  def clean_username(self):
    username = self.cleaned_data['username']
    (user, domain) = username.split('@', 1)
    if re.match(FormConst.Invite.DOMAIN_REGEX_YAHOO, domain):
      self.cleaned_data['type'] = 'yahoo'
    elif re.match(FormConst.Invite.DOMAIN_REGEX_GMAIL, domain):
      self.cleaned_data['type'] = 'gmail'
    else:
      raise forms.ValidationError(FormConst.Invite.DOMAIN_SUPPORT)

    return username

class InviteFormPeople(forms.Form):
  people = forms.MultipleChoiceField(label=FormConst.Invite.PEOPLE,
                                     widget=forms.CheckboxSelectMultiple)

  def __init__(self, * args, ** kwargs):
    if 'choices' in kwargs:
      choices = kwargs['choices']
      del kwargs['choices']
    else:
      choices = ()
    
    super(InviteFormPeople, self).__init__(*args, ** kwargs)

    self.fields['people'].choices = choices
    




