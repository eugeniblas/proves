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
from .forms import PostForm
from .models import Buzz


# Create your views here.
def index(request):
    if(request.user.is_authenticated):
        return render(request, 'testLogin.html')
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
            request.session.set_expiry(300);
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
#View where we'll have all our posts
def post_list(request):
    posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'post_list.html', {'posts': posts})