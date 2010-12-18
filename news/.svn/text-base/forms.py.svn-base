from const import FormConst
from django import forms
from django.forms.widgets import HiddenInput
from news.models import News
from widgets import UsersDynamicTextInput

__author__ = "Alexandru Palade <alexandru.palade@loopback.ro>"
__date__ = "$${date} ${time}$"

class AddNewsForm(forms.ModelForm):
  fb_wall = forms.BooleanField(required=False, label=FormConst.News.FB_WALL)
  
  def __init__(self, * args, ** kwargs):
    super(AddNewsForm, self).__init__(*args, ** kwargs)

    self.fields['anonymous'].label = FormConst.News.ANONYMOUS
    self.fields['anonymous'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['about_name'].label = FormConst.News.ABOUT_NAME
    self.fields['about_name'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['title'].label = FormConst.News.TITLE
    self.fields['title'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['text'].label = FormConst.News.TEXT
    self.fields['text'].error_messages = {'required': FormConst.REQUIRED}
    
    self.fields['video'].label = FormConst.News.VIDEO
    self.fields['video'].error_messages = {'required': FormConst.REQUIRED}


  class Meta:
    model = News
    fields = ('anonymous', 'about_name', 'about_id', 'title', 'text', 'video')
    widgets = {
      'about_id': HiddenInput(),
      'about_name': UsersDynamicTextInput(),
    }

class AddNewsInlineForm(forms.ModelForm):
  fb_wall = forms.BooleanField(initial=True, required=False,
                               label=FormConst.News.FB_WALL)
  
  def __init__(self, * args, ** kwargs):
    super(AddNewsInlineForm, self).__init__(*args, ** kwargs)

    self.fields['anonymous'].label = FormConst.News.ANONYMOUS
    self.fields['anonymous'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['about_name'].label = FormConst.News.ABOUT_NAME
    self.fields['about_name'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['text'].label = FormConst.News.TEXT
    self.fields['text'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['title'].label = FormConst.News.TITLE
    self.fields['title'].error_messages = {'required': FormConst.REQUIRED}

    self.fields['video'].label = FormConst.News.VIDEO
    self.fields['video'].error_messages = {'required': FormConst.REQUIRED}

  def clean_about_name(self):
    name = self.cleaned_data.get('about_name', '').title()
    return name

  def clean_title(self):
    return self.cleaned_data.get('title', '').title()

  class Meta:
    model = News
    fields = ('anonymous', 'about_id', 'about_name', 'title', 'text', 'video')
    widgets = {
      'about_id': HiddenInput(),
      'about_name': UsersDynamicTextInput(),
    }



