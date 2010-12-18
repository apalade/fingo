import datetime
from django import forms
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget

from const import FormConst
from profile.models import Profile
from widgets import CityDynamicTextInput


__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"

curr_year = datetime.date.today().year

class LoginForm(forms.Form):
  username = forms.CharField(label=FormConst.Register.USERNAME)
  password = forms.CharField(label=FormConst.Register.PASSWORD,
                             widget=forms.PasswordInput, min_length=3)


class RegisterForm(forms.ModelForm):
  email = forms.EmailField(label=FormConst.Register.EMAIL, required=True,
                           error_messages={'required': FormConst.REQUIRED})

  password2 = forms.CharField(label=FormConst.Register.PASSWORD2,
                              widget=forms.PasswordInput,
                              min_length=3,
                              error_messages={'required': FormConst.REQUIRED})


  def __init__(self, * args, ** kwargs):
    super(RegisterForm, self).__init__(*args, ** kwargs)

    self.fields['username'].label = FormConst.Register.USERNAME
    self.fields['username'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['password'].label = FormConst.Register.PASSWORD
    self.fields['password'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['email'].label = FormConst.Register.EMAIL
    self.fields['email'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['first_name'].label = FormConst.Register.FIRST_NAME
    self.fields['first_name'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['last_name'].label = FormConst.Register.LAST_NAME
    self.fields['last_name'].error_messages = {'required': FormConst.REQUIRED}



  """
  def clean_username(self):
    username = self.cleaned_data.get('username')
    try:
      User.objects.get(username=username)
    except User.DoesNotExist:
      return username
    raise forms.ValidationError(FormConst.Register.UNIQUE)"""

  def clean_first_name(self):
    first = self.cleaned_data.get('first_name').capitalize()
    return first

  def clean_last_name(self):
    last = self.cleaned_data.get('last_name').capitalize()
    return last


  def clean_email(self):
    email = self.cleaned_data.get('email')
    try:
      User.objects.get(email=email)
    except User.DoesNotExist:
      return email
    raise forms.ValidationError(FormConst.Register.UNIQUE)

  def clean_password2(self):
    passwd = self.cleaned_data.get('password')
    passwd2 = self.cleaned_data.get('password2')
    if passwd != passwd2:
      raise forms.ValidationError(FormConst.Register.DIFFERENT)
    return passwd
  
  
  class Meta:
    model = User
    widgets = {
      'password': forms.PasswordInput,
    }
    fields = ('username', 'password', 'email', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
  first_name = forms.CharField(label=FormConst.Register.FIRST_NAME, required=False)
  last_name = forms.CharField(label=FormConst.Register.LAST_NAME, required=False)
  password = forms.CharField(label=FormConst.Register.PASSWORD,
                             widget=forms.PasswordInput(render_value=False),
                             required=False)
  password2 = forms.CharField(label=FormConst.Register.PASSWORD2,
                              widget=forms.PasswordInput(render_value=False),
                              required=False)


  def clean_password2(self):
    passwd = self.cleaned_data.get('password')
    passwd2 = self.cleaned_data.get('password2')

    if passwd == '' and passwd2 == '':
      return self.cleaned_data
    
    if passwd != passwd2:
      raise forms.ValidationError(FormConst.Register.DIFFERENT)

    if len(passwd) < 3:
      raise forms.ValidationError(FormConst.Register.TOO_SHORT)
    
    return self.cleaned_data
  

  class Meta:
    model = Profile
    fields = ('gender', 'bday', 'city_curr', 'city_home', 'photo')
    widgets = {
      'bday': SelectDateWidget(years=range(curr_year - 5, curr_year - 75, -1)),
      'city_curr': CityDynamicTextInput(),
      'city_home': CityDynamicTextInput(),
    }
  
  