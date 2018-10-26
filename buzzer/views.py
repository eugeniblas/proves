from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from .models import Buzz
from django.contrib.auth import login, authenticate, logout


# Create your views here.
def index(request):
    return render(request, 'testLogin.html')

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


def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect(reverse("index"))

def searchView(request):
    # Redirect to a success page.
    return render(request, 'search.html')

