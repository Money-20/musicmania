from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from .forms import signUpForm, loginForm, CreateUserForm, ProfileForm, TrackForm

from .models import myUser, TrackModel, ProfileModel

from django.urls import reverse

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


    context = {
        'user': user,
        'all': all,
    }



    return render(request, 'index.html', context)
# to update/ create profile
@login_required(login_url='login')
def ProfileUpdate(request, id):

    user = myUser.objects.get(id = int(id))
    # myProfile = ProfileModel(user = user)
    # myProfile = myProfile.save()
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/index/{id}')

    context = {
        'form': form
    }
    return render(request, 'profileupdate.html', context)

# to display profile

@login_required(login_url='login')
def Profile(request, id):

    user = myUser.objects.get(id = id)
    myProfile = ProfileModel.objects.get(user = user)
    form = ProfileForm(instance=myProfile)
    pic = myProfile.dp.url
    myTracks = TrackModel.objects.all().filter(author = id)
    context = {
        'user': form,
        'id': id,
        'pic': pic,
        'tracks': myTracks
    }

    return render(request, 'profile.html', context)

@login_required(login_url='login')
def MusicUpload(request, id):
    
    form = TrackForm()

    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/index/{id}')
    
    context ={
        'form': form
    }
    return render(request, 'musicupload.html', context)

@login_required(login_url='login')
def MusicView(request, id):

    user = myUser.objects.get(id = id)
    myTracks = TrackModel.objects.all().filter(author = id)
    

    context = {
        'tracks' : myTracks, 

    }

    return render(request, 'tracks.html', context)

