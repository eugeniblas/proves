from django.conf.urls import url
from . import views

urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    # Authentication
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
    
    # Search
    url(r'^search/$', views.searchView, name='search')
    
    #Extras
    #url(r'^new_post/$', views.post_new, name='post_new'),
    url(r'^profiles/$', views.profile, name='profile'),
    url(r'^profile/(?P<user>.*)/$', views.profile, name='profile'),    
    url(r'^buzzs/$', views.buzzs, name='buzzs'),
    url(r'^buzzs/(?P<user>.*)/$', views.buzzs, name='buzzs')   
]

