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

    songName = models.CharField(max_length=20, null=True, blank=True)
    songImg = models.ImageField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)
    author = models.ForeignKey(myUser, on_delete=models.CASCADE, null=True, blank=True)

    #Todo: create a downloadable song Track with timeLength

    def __str__(self):
        return self.songName


class ProfileModel(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    dp = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True, max_length=1000)

    #Todo :create a list of all the tracks added


    def __str__(self):
        return self.user.username
#Todo : create a library containing a downloadable list of all the tracks ass with the user
