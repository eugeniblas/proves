from django.db import models
from django.contrib.auth.models import User


# Model Buser:  User for Buzzer
#   Buser has all attributes of User:
#   	username: it must begin with '@' !!!
#       first_name
#	last_name
#	email
#       password 
#       groups
#       user_permissions
#	is_staff
#	is_active
#	is_superuser
#	last_login
#	date_joined

class Buser (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=150)  # name that appears on screen
    location = models.CharField(max_length=150)  # defined location for user account’s profile
    url = models.CharField(max_length=150)  # URL provided by the user in association with their profile
    lang = models.CharField(max_length=150) # The BCP 47 code for the user’s self-declared user interface language
    def __str__(self):
        return(self.user.username + " - " + self.screen_name + " - " + self.user.first_name + " - " + self.user.last_name)
    def all_fields(self):
        return("username: " + self.user.username + "  password: " + self.user.password)


