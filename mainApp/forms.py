from django.forms import ModelForm
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
    class Meta:
        model =TrackModel
        fields = '__all__'