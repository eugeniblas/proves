from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
    
    # Search
    url(r'^search/$', views.searchView, name='search'),
    
    # Extras
    url(r'^new_post/$', views.post_new, name='post_new'),
    url(r'^profile/(?P<user>.*)/$', views.profile, name='profile'),
    url(r'^actualizarProfile/(?P<user>.*)/$', views.actualizarProfile, name='actualizarProfile'),

    # Browser DBs
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),  
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^profiles/(?P<user>.*)/$', views.profiles, name='profiles'),    
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs'),
    url(r'^upload/$', views.load_image, name='load_image'),
    url(r'^hashtags/$', views.hashtags, name='hashtags'),
    url(r'^hashtags/(?P<text_hashtag>.*)/$', views.hashtags, name='hashtags'),

    # Only Test
    url(r'^chatsList/$', views.chatsList, name='chatsList'),
    url(r'^chatsList/(?P<user>.*)/$', views.chatsList, name='chatsList'),
    url(r'^chatsUsers/$', views.chatsUsers, name='chatsUsers'),
    url(r'^chatsUsers/(?P<list_of_users>.*)/$', views.chatsUsers, name='chatsUsers'),
    url(r'^createMessage/$', views.createMessage, name='createMessage'),
    url(r'^createMessage/(?P<list_of_message>.*)/$', views.createMessage, name='createMessage'),
    url(r'^chatMessage/$', views.chatMessage, name='chatMessage'),
    url(r'^chatMessage/(?P<id_chat>.*)/$', views.chatMessage, name='chatMessage')



]

