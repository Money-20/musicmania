from django.contrib import admin
from .models import myUser, ProfileModel, TrackModel

# Register your models here.

admin.site.register(myUser)
admin.site.register(ProfileModel)
admin.site.register(TrackModel)
