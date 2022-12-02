from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class myUser(User):
    # name = models.CharField(max_length=25, null=True, blank=True)
    # email = models.EmailField(null=True, blank=True)
    # mobile = models.BigIntegerField(null=True, blank=True)
    # bio = models.TextField(null=True, blank=True, max_length=1000)
    dateCreated = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username



class TrackModel(models.Model):

    songName = models.CharField(max_length=20, null=True, blank=False)
    songImg = models.ImageField(null=True, blank=False)
    file = models.FileField(null=True, blank=False, default='static/images/file_example_MP3_700KB_DY8xrM5.mp3')
    author = models.ForeignKey(myUser, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.songName


class ProfileModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dp = models.ImageField(null=True, blank=True, default='static/images/turtle_TpDCiLF.jpeg')
    bio = models.TextField(null=True, blank=True, max_length=1000)
        # add a models.URLFIELD to create a contact link to the user
    contact = models.TextField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.username
#Todo : create a library containing a downloadable list of all the tracks ass with the user
