from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Buser


# Create your views here.
def index(request):
    return HttpResponse("Hello, this is Buzzer app")

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
