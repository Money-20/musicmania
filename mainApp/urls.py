
from django.urls import path
from .views import (Login, Logout, Register, Index, 
                    Profile, ProfileUpdate, MusicUpload, 
                    MusicView, Feed, AddToFav,  Favourite, 
                    RemoveFav, SendMail)
urlpatterns = [

    
    path('', Register, name = 'home'),
    path('register', Register, name='signUp'),
    path('login', Login, name='login'),
    path('index/<slug:id>', Index, name='index'),
    path('profile/<slug:id>', Profile, name= 'profile'),
    path('profileUpdate/<slug:id>', ProfileUpdate, name ='profileUpdate'),
    path('musicUpload/<slug:id>', MusicUpload, name='musicUpdate'), 
    path('tracks/<slug:id>', MusicView, name='musicView'),
    path('logout', Logout, name='logout'),
    path('feed/<slug:id>', Feed, name='feed'),
    path('addfav/<slug:id>/<slug:key>', AddToFav, name='addFavourite'),
    path('favourites/<slug:id>', Favourite, name="favourites"),
    path('removefav/<slug:id>/<slug:key>', RemoveFav, name="removeFavourite"),
    path('mail/<slug:id>', SendMail, name="sendMail"),    
]