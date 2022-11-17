from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .forms import signUpForm, loginForm, CreateUserForm, ProfileForm, TrackForm

from .models import myUser, TrackModel, ProfileModel

from django.urls import reverse

def CreateProfile(user):
    try:
        profile = ProfileModel.objects.get(user = user)
    except DoesNotExist:
        profile = ProfileModel.objects.create(user = user)
# Create your views here.
#
# class Home(TemplateView):
#     template_name = 'index.html'
#     extra_context = {'users': User.objects.all()}
#
# #
# # class Login(CreateView):
# #     form_class = loginForm
# #     success = reverse_lazy(Home)
# #     template_name = 'login.html'
# #     extra_context = {'form': form_class}
#
#
# class SignUp(CreateView):
#     form_class = signUpForm
#     success = reverse_lazy(Login)
#     template_name = 'signup.html'
#     extra_context = {'form': form_class}

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
        return redirect(f'index/{request.user.id}')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password=password )

            if user is not None:
                CreateProfile(user)
                login(request, user)
                return HttpResponse('login Success!')

            else:
                pass
        context = {

        }
        return render(request, 'login.html', context)
def Logout(request):
    logout(request)
    return HttpResponse('logout success!')

@login_required(login_url='login')
def Index(request, id):
    user = request.user
    all = myUser.objects.get(id = id)
    id = id
    CreateProfile(user)
    context = {
        'user': user,
        'all': all,
        'id' : id
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
        'pic': pic
    }
    return render(request, 'profileupdate.html', context)

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
    context = {
        'user': form,
        'id': id,
        'pic': pic,
        'tracks': myTracks,
        'username' : username,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def MusicUpload(request, id):

    user = myUser.objects.get(id = int(id)) 
    ## it is adding an extra model every time the endpoint is accessed
    # myModel = TrackModel.objects.(author = user)
    form = TrackForm({'author': user.id})

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/index/{id}')
    
    context ={
        'form': form,
        'user': user,
    }
    return render(request, 'musicupload.html', context)

@login_required(login_url='login')
def MusicView(request, id):
    user = myUser.objects.get(id = id)
    try:
        music = TrackModel.objects.all().filter(author = id)[0]
    except IndexError:
        context = {'id' : id}
        return render(request, 'nolibrary.html', context)
    
    myTracks = TrackModel.objects.all().filter(author = id)

    context = {
        'tracks' : myTracks, 

    }

    return render(request, 'tracks.html', context)

def CreateProfile(user):
    try:
        profile = ProfileModel.objects.get(user = user)
    except:
        profile = ProfileModel.objects.create(user = user)