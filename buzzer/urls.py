from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Database users
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),

    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),

    # Database user profiles
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^profiles/(?P<user>.*)/$', views.profiles, name='profiles'),

    # Database buzzs
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs'),


    # Search
    url(r'^search/(?P<search_text>.*)/$', views.userSearch, name='userSearch')
]
