from django.forms import ModelForm
from django import forms
from .models import myUser, ProfileModel, TrackModel
from django.contrib.auth.forms import UserCreationForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = myUser
        fields = ['username', 'email', 'password1', 'password2']

class signUpForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'email', 'password']

class loginForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['username', 'password']

class ProfileForm(ModelForm):
    class Meta:
        model = ProfileModel
        fields = '__all__'

class TrackForm(ModelForm):
    # body = forms.CharField(required=True, label="Enter Title of music")
    # image = forms.ImageField(required=True, label="Upload image")
    # FILE = forms.FileField(required=True, label="Upload music file")
    class Meta:
        model =TrackModel
        fields = '__all__'
        widgets = {'author':forms.HiddenInput()} 