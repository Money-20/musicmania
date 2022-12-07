
from django.urls import path
from .views import Login, Logout, Register, Index, Profile, ProfileUpdate, MusicUpload, MusicView, Feed, Favourite
urlpatterns = [

    # path('', Home.as_view(), name='homePage'),
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
    # path('fav/<slug:id>', Favourite, name='fav'),
    # path('search/<slug:id>', Search, name="search")
]