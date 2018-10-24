from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
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

# List All Users or List one (username)
def users(request, user=""):
    if user:
        response = "You're looking for user from %s <BR>" % user
        list_of_users = User.objects.filter(username=user)
        response = response + '<BR> <li>' + '<BR> <li>'.join([str(user.id) + " - " + str(user) for user in list_of_users])
    else:
        response = "You're looking all Users"
        list_of_users = User.objects.filter()
        response = response + '<BR> <li>' + '<BR> <li>'.join([str(user.id) + " - " + str(user) for user in list_of_users])

    return HttpResponse(response)

# List All Users+Profile or List one (username)
def profiles(request, user=""):
    if user:
        response = "You're looking for user from %s <BR>" % user
        list_of_users = User.objects.filter(username=user)
        response = response + '<BR> <li>' + '<BR> <li>'.join([Profile.all_fields(user.profile) for user in list_of_users])
    else:
        response = "You're looking all Users"
        list_of_users = User.objects.filter()
        response = response + '<BR> <li>' + '<BR> <li>'.join([Profile.all_fields(user.profile) for user in list_of_users])

    return HttpResponse(response)

# List All Buzzs or List of one username
def buzzs(request, user=""):
    if user:
        response = "You're looking for buzz of user from %s <BR>" % user
        list_of_users = User.objects.filter(username=user)
        for userlist in list_of_users:
            list_of_buzzs = Buzz.objects.filter(user_id=userlist.id)
            response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])
    else:
        response = "You're looking all Users"
        list_of_buzzs = Buzz.objects.filter()
        response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])

    return HttpResponse(response)


def signupView(request):

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if user is not None:
            #fer saltar una alerta que l'usuari ja existeix
            return render(request, "signup.html")

        else:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            if user is not None:
                if user.is_active:  # Active user are not banned users
                    login(request, user)
                    # Redirect to a success page.
                    return HttpResponseRedirect(reverse('index'))

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


def profile(request, user=""):  # TEMPORAL
    if request.method == "GET":
        profile = User.objects.filter(username=user)
        posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
        form = PostForm()        
        
        args = {'posts': posts, 'form': form, 'profile': profile.first()}    
        
        return render(request, 'profile.html', args)

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()                        

            return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))

"""
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            return render(request,'testLogin.html')
    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})
"""

def userSearch(request, search_text):
    usernameSearch = Profile.objects.filter(user__username__contains=search_text)
    profileSearch= Profile.objects.filter(screen_name__contains=search_text)
    fullSearch = chain(usernameSearch, profileSearch)

    response = "<br> Users: <br>"
    response += '<br> <li>' + '<li>'.join([str(s) for s in fullSearch]) + "</li> <br>"
    return response


def buzzSearch(request, search_text):
    search = Buzz.objects.filter(text__contains=search_text)

    response = "Buzzs: <br>"
    response += '<br> <li>' + '<br> <li>'.join([str(s.all_fields()) for s in search]) + "</li> <br>"
    return response


def searchView(request, search_text):
    response = "Search: %s <br>" % search_text
    response += userSearch(request, search_text) + buzzSearch(request, search_text)
    return HttpResponse(response)
