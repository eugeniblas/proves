from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
<<<<<<< HEAD
    url(r'^search/$', views.searchView, name='search'),
]
=======
    url(r'^profiles/$', views.profiles, name='profiles'),
    url(r'^profiles/(?P<user>.*)/$', views.profiles, name='profiles'),
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs')   
]
>>>>>>> SP-2
