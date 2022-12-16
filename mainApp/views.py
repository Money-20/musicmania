from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .forms import signUpForm, loginForm, CreateUserForm, ProfileForm, TrackForm, SearchForm, EmailForm

from .models import myUser, TrackModel, ProfileModel, FavouriteModel

from django.urls import reverse

from django.core.mail import send_mail

from django.conf import settings


def CreateProfile(user):
    try:
        profile = ProfileModel.objects.get(user = user)
    except:
        profile = ProfileModel.objects.create(user = user)

def Register(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                mail = form.cleaned_data.get('email')

                return redirect('login')
        context = {'form' : form}

        return render(request,'signup.html', context)

def Login(request):

    if request.user.is_authenticated:
        return redirect(f'/index/{request.user.id}')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password=password )

            if user is not None:
                login(request, user)
                return redirect(f'/index/{request.user.id}')

            else:
                return HttpResponse('You have no account! You need to register first')
        context = {

        }
        return render(request, 'login.html', context)


def Logout(request):
    logout(request)

    return redirect('login')
    # return HttpResponse('logout success!')

@login_required(login_url='login')
def Index(request, id):
    # auto create an empty profile for the new user 
    user = myUser.objects.get(id = int(id))
    try:
        profile = ProfileModel.objects.get(user = user)
    except :
        profile = ProfileModel.objects.create(user = user)

    user = request.user
    all = myUser.objects.get(id = id)
    id = id
    user = myUser.objects.get(id = int(id))
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url
    # CreateProfile(user)
    context = {
        'user': user,
        'all': all,
        'id' : id,
        'pic' : pic
    }



    return render(request, 'index.html', context)
# to update/ create profile
@login_required(login_url='login')
def ProfileUpdate(request, id):

    user = myUser.objects.get(id = int(id))
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url
    # myProfile = myProfile.save()
    form = ProfileForm(instance=myProfile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=myProfile)
        if form.is_valid():
            form.save()
            return redirect(f'/profile/{id}')

    context = {
        'form': form, 
        'pic': pic,
        'id': id,
    }
    return render(request, 'updateprofile.html', context)

# to display profile

@login_required(login_url='login')
def Profile(request, id):
    user = myUser.objects.get(id = int(id))
    try:
        profile = ProfileModel.objects.get(user = user)
    except :
        profile = ProfileModel.objects.create(user = user)
    user = myUser.objects.get(id = int(id))
    username = user.username
    myProfile = ProfileModel.objects.get(user = user)
    form = ProfileForm(instance=myProfile)
    pic = myProfile.dp.url
    myTracks = TrackModel.objects.all().filter(author = id)
    numOfSongs = len(list(myTracks))
    bio = myProfile.bio
    context = {
        'user': form,
        'id': id,
        'pic': pic,
        'tracks': myTracks,
        'username' : username,
        'numberofsongs': numOfSongs,
        'bio': bio,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def MusicUpload(request, id):

    user = myUser.objects.get(id = int(id)) 
    ## it is adding an extra model every time the endpoint is accessed
    # myModel = TrackModel.objects.(author = user)
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url
    form = TrackForm({'author': user.id})

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES, {'author' : user.id})
        if form.is_valid():
            form.save()
            return redirect(f'/index/{id}')
    
    context ={
        'form': form,
        'user': user,
        'pic': pic,
        'id': id,
    }
    return render(request, 'uploadmusic.html', context)

@login_required(login_url='login')
def MusicView(request, id):
    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url

    try:
        music = TrackModel.objects.all().filter(author = id)[0]
    except IndexError:
        context = {'id' : id}
        return render(request, 'nolibrary.html', context)
    
    myTracks = TrackModel.objects.all().filter(author = id)
    favs = FavouriteModel.objects.filter(belongsto = myProfile)
    favlist = [i.trackid for i in list(favs)]

    if request.method == 'GET':
        query = request.GET.get('query')
        try:
            tracks = TrackModel.objects.filter(songName__icontains = query)    
            context = {
                'tracks' : tracks,
                'user' : user,
                'pic' : pic, 
                'id' : id,
            }   
            return render(request, 'tracks.html', context)               
        except:
            pass
    context = {
        'tracks' : myTracks, 
        'user' : user,
        'pic' : pic,
        'id' : id,
        'ls' : favlist,
    }

    return render(request, 'tracks.html', context)
## Error handling for empty Profiles
# def CreateProfile(user):
#     try:
#         profile = ProfileModel.objects.get(user = user)
#     except:
#         profile = ProfileModel.objects.create(user = user)


# Feed containing all the tracks along with INFO in timely order
@login_required(login_url='login')
def Feed(request, id):
    tracks = TrackModel.objects.all()
    user = myUser.objects.get(id= id)
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url

    favs = FavouriteModel.objects.filter(belongsto = myProfile)
    alltracks = [i.id for i in list(tracks)]
    favlist = [i.trackid for i in list(favs)]
    print(alltracks)
    print(favlist)

    if request.method == 'GET':
        query = request.GET.get('query')
        try:
            tracks = TrackModel.objects.filter(songName__icontains = query)    
            print(tracks)
            context = {
                'tracks' : tracks,
                'user' : user,
                'pic' : pic, 
                'id' : id,
                'ls' :favlist,
            }   
            return render(request, 'feed.html', context)               
        except:
            pass



    
    context = {
        'tracks' : tracks,
        'user' : user,
        'pic' : pic, 
        'id' : id,
        'ls' : favlist,
    }

    return render(request, 'feed.html', context)

# Todo: Search functionaility of tracks::DOne
# Todo: Favourite list ::DOne
# Todo: Create Direct Mail from one to another using forms
# Todo: Sponsorship to artists by integrating razorpay API

# function to add to fav
@login_required(login_url='login')
def AddToFav(request, id, key):
    # id --> id of the user
    # key --> id of the m
    # usic track
    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)

    try:
        favTrack = FavouriteModel.objects.get(trackid = key)
    except:
        favTrack = FavouriteModel.objects.create(trackid = key, belongsto = myProfile)

    return redirect(f'/favourites/{id}')

@login_required(login_url='login')
def RemoveFav(request, id, key):
    # id --> id of the user
    # key --> id of the music track
    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)

    try:
        favtrack = FavouriteModel.objects.filter(trackid = key)
        favtrack.delete()
    except:
        print('delete unsuccessful')
    
    return redirect(f'/favourites/{id}')


# function to display the favourite songs
@login_required(login_url='login')
def Favourite(request, id):

    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url
    favs = FavouriteModel.objects.filter(belongsto = myProfile)
    favlist = [i.trackid for i in list(favs)]

    if len(favs) < 1:
        return HttpResponse('Your favourites section is empty')   
    
    tracks = []
    
    for i in favlist:
        tracks.append(TrackModel.objects.get(id = i))
    
    context = {
        'tracks' : tracks,
        'user' : user,
        'pic' : pic, 
        'id' : id,
    }

    return render(request, 'favourites.html', context)

def SendMail(request,id):

    # create a variable to keep track of the form
    messageSent = False
    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)
    pic = myProfile.dp.url
    sender = user.username

    # check if form has been submitted
    if request.method == 'POST':

        form = EmailForm(request.POST)

        # check if data from the form is clean
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{sender} sent a message"
            message = cd['message']
            reciever = cd['recipient']
            recieverMail = myUser.objects.get(username = reciever).email

            # send the email to the recipent
            send_mail(subject, message,
                      settings.DEFAULT_FROM_EMAIL, [recieverMail])

            # set the variable initially created to True
            messageSent = True

    else:
        form = EmailForm()

    return render(request, 'sendmail.html', {

        'form': form,
        'user': user,
        'pic' : pic,
        'messageSent': messageSent,
        'id' :id

    })

