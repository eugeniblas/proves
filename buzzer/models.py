from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User:  auth_user (contrib.auth.User)
#   user of Buzzer
#   attributes of User:
#     id (integer- primary key - autoincrement)
#     username (varchar(128) - not null)
#     first_name (varchar(30) - not null)
#     last_name (varchar(150) . not null)
#     email (varchar(254) - not null)
#     password (varchar(128) - not null)
#     is_staff (boolean - not null)
#     is_active (boolean - not null)
#     is_superuser (boolean - not null)
#     last_login (datetime - null)
#     date_joined (datetime - null)

# Profile: buzzer_profile
#   extension User (one to one)
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=50)  # name that appears on screen (complementary username)    
    location = models.CharField(max_length=150)  # defined location for user account’s profile
    url = models.CharField(max_length=150)  # URL provided by the user in association with their profile
    bio = models.CharField(max_length=150) # general information about user 
    birthday = models.DateField(auto_now=False, auto_now_add=False,null=True) # user's birthday 
    
    def __str__(self):
        return(self.user.username + " - " + self.screen_name + " - " + self.user.first_name + " - " + self.user.last_name)
    def all_fields(self):
        return("username: " + self.user.username + "  password: " + self.user.password)


from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

