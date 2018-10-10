from comtypes.automation import _
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Buser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    if(request.user.is_authenticated):
        return render(request,'Home_Page.html')
    else:
        return render(request, 'login.html')


# List All Users o List one (username)
def users(request, user=""):
    if user:
        response = "You're looking for user from %s <BR>" % user
        list_of_users = User.objects.filter(username=user)
        response = response + '<BR> <li>' + '<BR> <li>'.join([Buser.all_fields(user.buser) for user in list_of_users])
    else:
        response = "You're looking all Users"
        list_of_users = User.objects.filter()
        response = response + '<BR> <li>' + '<BR> <li>'.join([Buser.all_fields(user.buser) for user in list_of_users])

    return HttpResponse(response)

def signupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Log in the user after the registration
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {'form': form})


def loginView(request):
    username = request.POST.get('username', '')
    print(username)
    password = request.POST.get('password', '')
    print(password)
    user = authenticate(username=username, password=password)
    print(user)


    if user is not None:
        if user.is_active:  # Active user are not banned users
            login(request, user)

            # Redirect to a success page.
            return HttpResponseRedirect(reverse('index'))
            #return render(request, 'Home_Page.html')

        else:   # User is banned
            raise forms.ValidationError(_("This account is banned."), code='inactive',)
    else:
        # Show an error page
        return render(request, 'login.html')


def logoutView(request):
    logout(request)
    # Redirect to a success page.
    return render(request, 'login.html')

