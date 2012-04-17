import re
from django.contrib.auth.models import User
from django import forms


"""
class ProfileSettingsForm(form.Form):
    charCount = forms.IntegerField(
        label=u'What is the minimum number of characters a word must contain to be of special interest?',
        widget=forms.IntegerField
    )
    wordCount = forms.IntegerField(
        label=u'And how many times must a word have appeared in the text?',
        widget=forms.IntegerField
    )
"""


class CorpusSaveForm(forms.Form):
    file = forms.FileField(
        label  = u'Text File',
        widget = forms.ClearableFileInput()
    )
    title = forms.CharField(
        label  = u'Title',
        widget = forms.TextInput(attrs={'size':64})
    )
    tags = forms.CharField(
        label    = u'Tags',
        required = False,
        widget   = forms.TextInput(attrs={'size':64})
    )

class SearchForm(forms.Form):
    query = forms.CharField(
        label  = u'Enter a keyword to search for',
        widget = forms.TextInput (attrs={'size':32})
    )

class UploadFileForm(forms.Form): #todo: add functions for cleaning file uploads: ensure they are unicode, strip metadata and encode as yaml
    file = forms.FileField(
        label  = u'Text File',
        widget = forms.FileInput()
    )

#todo clean_metadata_doc
def clean_metadata_doc(self):
    return

#todo clean_metadata_xml
def clean_metadata_xml(self):
    return

#todo turn_to_yaml
def turn_to_yaml(self):
    return


class RegistrationForm(forms.Form): # new users register using this form
    username   = forms.CharField(label=u'Username', max_length=30)
    email      = forms.EmailField(label=u'Email')
    password1  = forms.CharField(
        label  = u'Password',
        widget = forms.PasswordInput()
    )
    password2  = forms.CharField(
        label  = u'Password (Again)',
        widget = forms.PasswordInput()
    )

def clean_password2(self): # password validation
    if 'password1' in self.cleaned_data:
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2:
            return password2
    raise forms.ValidationError('Passwords do not match.')

def clean_username(self): # ensure username is a valid string and is unique
    username = self.cleaned_data['username']
    if not re.search(r'^\w+$', username):
        raise forms.ValidationError('Username can only contain '
                                    'alphanumeric characters and the underscore.')
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return username
    raise forms.ValidationError("Username is already taken.")
