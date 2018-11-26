from AptUrl.Helpers import _
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Buzz, Hashtag, Chat, Message
from .forms import PostForm, ProfileForm, Profile2Form
from itertools import chain
from django.contrib.auth import login, authenticate, logout
 


# Create your views here.
def index(request):
    if (request.user.is_authenticated):
        form = PostForm()
        return render(request, 'testLogin.html', {'form': form})
    else:
        return render(request, "signup.html")


# List All Users or List one (username)
def users(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [str(user.id) + " - " + str(user) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [str(user.id) + " - " + str(user) for user in list_of_users])
    return HttpResponse(response)


# List All Users+Profile or List one (username)
def profiles(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for user from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Profile.all_fields(user.profile) for user in list_of_users])
        else:
            response = "You're looking all Users"
            list_of_users = User.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Profile.all_fields(user.profile) for user in list_of_users])
    return HttpResponse(response)


# List All Buzzs or List of one username
def buzzs(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
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
        first_name = request.POST.get('name', '')
        last_name = request.POST.get('surname', '')
        email = request.POST.get('email', '')
        screen_name = request.POST.get('usertag', '')

        user = authenticate(username=username, password=password)

        if user is not None:
            # mensage de error ja existeix

            return render(request, "signup.html")

        else:
            user = User.objects.create_user(username=username, password=password)
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
            # mensage de error
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

        else:  # User is banned
            raise forms.ValidationError(_("This account is banned."), code='inactive', )
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
    profileSearch = Profile.objects.filter(screen_name__contains=search_text)
    fullSearch = usernameSearch | profileSearch
    response = [s for s in fullSearch]
    return response


def buzzSearch(request, search_text):
    search = Buzz.objects.filter(text__contains=search_text)
    response = [s for s in search]
    return response


def searchView(request):
    search_text = request.POST.get('search_text')

    if request.method == "POST":
        users = userSearch(request, search_text)
        buzzs = buzzSearch(request, search_text)
        args = {'users': users, 'buzzs': buzzs, 'search_text': search_text}
        return render(request, 'search.html', args)

    return render(request, 'search.html')

def actualizarProfile(request, user=""):
    form2 = Profile2Form(request.POST)
    if form2.is_valid():
        first_name = form2.cleaned_data['first_name']
        last_name = form2.cleaned_data['last_name']
        email = form2.cleaned_data['email']
        location = form2.cleaned_data['location']
        screen_name = form2.cleaned_data['screen_name']
        url = form2.cleaned_data['url']
        bio = form2.cleaned_data['bio']
        birthday = form2.cleaned_data['birthday']
        usuario = User.objects.filter(username=request.user).first()
        profile = usuario.profile

        if first_name != '':
            usuario.first_name = first_name
        if last_name != '':
            usuario.last_name = last_name
        if email != '':
            usuario.email = email
        if screen_name != '':
            profile.screen_name = screen_name
        if location != '':
            profile.location = location
        if url != '':
            profile.url = url
        if bio != '':
            profile.bio = bio
        if birthday != '':
            profile.birthday = birthday

        profile.save()
        usuario.save()

        return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))
    return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))


def profile(request, user=""):  # TEMPORAL
    if request.method == "GET":
        profile = User.objects.filter(username=user)
        posts = Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
        form = PostForm()        
        form2 = Profile2Form()
        args = {'posts': posts, 'form': form, 'form2': form2, 'profile': profile.first()}


        return render(request, 'profile.html', args)

    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()
            post.save()
            # find hashtags and set buzzs in its hashtag
            hashtags_possible = re.findall(r'(##+)|#(\w+#)|#(\w+)',post.text)
            list_of_hashtags = []
            for pair in hashtags_possible:
                for i in range(3):	
                    if pair[i] != '' and pair[i].find('#')==-1:
                        if pair[i] not in list_of_hashtags:
                            list_of_hashtags.append(pair[i])        
            for tag in list_of_hashtags:
                if Hashtag.objects.filter(text = tag).exists():
                    hashtag = Hashtag.objects.filter(text = tag)[0]
                else: 
                    hashtag = Hashtag.objects.create(text = tag)
                hashtag.buzzs.add(post)
                hashtag.save()

            return HttpResponseRedirect(reverse("profile", kwargs={'user': user}))



@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published_date = timezone.now()

            # If there is a file attached we save the file and file type in the database
            file = request.FILES.get('file', None)
            if file:
                post.file = file
                # Getting file type from MIME
                post.file_type = file.content_type.split('/')[0]

            if isMultimedia(post.file_type):
                post.save()
            else:
                messages.error(request, "El archivo introducido no es un archivo multimedia")

        return HttpResponseRedirect(reverse("profile", kwargs={'user': request.user.username}))

    else:
        form = PostForm()
    return render(request, 'post_edit.html', {'form': form})


def isMultimedia(type): # Returns true if the file is multimedia, or if there's no file
    return type == 'image' or type == 'video' or type == 'audio' or type == ''

def load_image(request):
    instance = get_object_or_404(Profile, user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.image = request.FILES['image']
            instance.save()

            return HttpResponseRedirect(reverse("profile", kwargs={'user': request.user.username}))

    else:
        form = ProfileForm()

    return render(request, 'edit.html', {'form': form})



# List All Buzzs or List of one hashtag
def hashtags(request, text_hashtag=""):
    #print(text_hashtag)
    response = "You aren't admin"
    p = posts_hashtags(request.user,text_hashtag)
    #print(p)
    if request.user.is_superuser:
        if text_hashtag:
            response = "You're looking for buzz of hashtag from %s <BR>" % text_hashtag
            list_of_hashtags = Hashtag.objects.filter(text=text_hashtag)

            for hashtaglist in list_of_hashtags:
                list_of_buzzs = hashtaglist.buzzs.all()
                response = response + '<BR> <li>' + '<BR> <li>'.join([Buzz.all_fields(buzz) for buzz in list_of_buzzs])
        else:
            response = "You're looking all hashtags"
            list_of_hashtags = Hashtag.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join([str(hashtag) for hashtag in list_of_hashtags])

    return render(request,'find_tags.html',{'response':response,'list_post':p,'tag':text_hashtag})

def posts_hashtags(user,tag):
    posts =Buzz.objects.filter(published_date__lte=timezone.now()).order_by('published_date').filter(user__username=user)
    post_list = []
    for post in posts:
        for palabra in post.text.split():
            #print(palabra,tag)
            if(palabra==tag): # El post tiene el tag
                post_list.append(post)
                break
    return post_list


# define equal in lists
def equal_list(list1,list2):
    list1.sort()
    list2.sort()
    equals = True
    if len(list1) != len(list2):
        equals = False
    else:
        for i in range(len(list1)):
            if list1[i] != list2[i]:
                equals = False
                break

    return equals

# search list of chats of one user
def search_chats(user_name):
    userchat = User.objects.get(username=user_name)
    list_of_chats = userchat.chat_set.all()
    return list_of_chats

# create a chat and return
def create_chat(users_list,chat_name=""):     
    if chat_name:
        chat = Chat.objects.create(name=chat_name)
    else:
        for user in users_list:
            chat_name += str(user.username) 
        chat = Chat.objects.create(name=chat_name)
    chat.members.set(users_list)
 
    chat.save()

    return chat

# search chat of a list of users  (if the chat doesnt exist it will be created)
#    enter a list of names of all users (first sender)
#    return chat 
def search_chat(list_of_user_names):
    list_of_chats = search_chats(list_of_user_names[0])
    found = False
    list_of_member_names = []
    
    for chat in list_of_chats:
        list_of_member_names = []
        for member in  chat.members.all():
            list_of_member_names.append(member.username)
        if equal_list(list_of_member_names,list_of_user_names):
            found= True
            chat_return = chat
            break

    if (not found):
       list_of_users = []
       for user_name in list_of_user_names:
           user = User.objects.get(username=user_name)
           list_of_users.append(user)
       chat_return = create_chat(list_of_users)
    
    return chat_return

# create message 
def create_message(chat_id,user_name,text_message):
    chat = Chat.objects.get(id_chat=chat_id)
    user = User.objects.get(username = user_name)
    message = Message.objects.create(chat=chat,user=user)
    message.date = timezone.now()
    message.content = text_message
    message.save()
    return message 

# return all messages of a chat ordered by date
def messages_chat(chat_id):
    chat = Chat.objects.get(id_chat=chat_id)
    #list_of_messages = sorted(chat.messages.all , key = lambda x: x.object.time)
    list_of_messages = chat.message_set.all()
    return list_of_messages

# List All chats of an user  ***ONLY TEST***
def chatsList(request, user=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if user:
            response = "You're looking for chats from %s <BR>" % user
            list_of_users = User.objects.filter(username=user)
            list_of_chats = list_of_users[0].chat_set.all()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Chat.all_fields(chat) for chat in list_of_chats])
        else:
            response = "You're looking all chats"
            list_of_chats = Chat.objects.filter()
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Chat.all_fields(chat) for chat in list_of_chats])
    return HttpResponse(response)

# find chat of a list of users   ***ONLY TEST***
def chatsUsers(request, list_of_users=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if list_of_users:
            response = "You're looking for chats from %s <BR>" % list_of_users
            W = list_of_users.split(",")
            chat = search_chat(W)
            response = response + Chat.all_fields(chat)
        else:
            response = "NO list"
             
    return HttpResponse(response)

# find chat of a list of users   ***ONLY TEST***
def createMessage(request, list_of_message=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if list_of_message:
            response = "You're looking for chats from %s <BR>" % list_of_message
            W = list_of_message.split(",")
            #sender = list_of_users[0]
            #response = response + " +  " + str(list_of_usersW[0])
            message = create_message(W[0],W[1],W[2])
            if message:
                response = response + Message.all_fields(message)
        else:
            response = "NO list"
             
    return HttpResponse(response)

# messages of a chat   ***ONLY TEST***
def chatMessage(request, id_chat=""):
    response = "You aren't admin"
    if request.user.is_superuser:
        if id_chat:
            response = "You're looking for chats from %s <BR>" % id_chat
            list_of_messages = messages_chat(id_chat)
            response = response + '<BR> <li>' + '<BR> <li>'.join(
                [Message.all_fields(message) for message in list_of_messages])            
        else:
            response = "NO list"
             
    return HttpResponse(response)



