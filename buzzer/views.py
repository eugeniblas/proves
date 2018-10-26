from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .models import Buzz
from django.contrib.auth import login, authenticate, logout
from itertools import chain
from .forms import PostForm


# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        form = PostForm()
        return render(request, 'testLogin.html', {'form': form})
    else :
        return render(request, "signup.html")

      
def signupView(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        first_name = request.POST.get('name', '')
        last_name = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        screen_name = request.POST.get('usertag', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            # mensage de error ja existeix
            return render(request, "signup.html")

        else:
            user = User.objects.create_user(username=username,password=password)
            if user is not None:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.save()
                profile = Profile.objects.create(user=user)
                profile.screen_name = screen_name
                profile.save()
                if user.is_active:  # Active user are not banned users
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect(reverse('index'))
            #mensage de error
            return render(request, "signup.html")

    else:
        return render(request, "signup.html")


def loginView(request):
    username = request.POST.get('username', '')    
    password = request.POST.get('password', '')    
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:  # Active user are not banned users
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))

        else:   # User is banned
            raise forms.ValidationError(_("This account is banned."), code='inactive',)
    else:
        # Show an error page
        return render(request, 'login.html')


@login_required
def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse("index"))

def userSearch(request, search_text):
    usernameSearch = Profile.objects.filter(user__username__contains=search_text)
    profileSearch= Profile.objects.filter(screen_name__contains=search_text)
    fullSearch = usernameSearch | profileSearch

    response = [s for s in fullSearch]
    return response


def buzzSearch(request, search_text):
    search = Buzz.objects.filter(text__contains=search_text)

    response = [s for s in search]
    return response


def searchView(request):
    search_text = request.POST.get('search_text')
    users = userSearch(request, search_text)
    buzzs = buzzSearch(request, search_text)
    response = ""
    for i in users:
        response += str(i.user)

    for i in buzzs:
        response += str(i.text)
    return render(request, 'search.html')

