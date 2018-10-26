from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),    
    url(r'^logout/$', views.logoutView, name='logout'),
    url(r'^search/$', views.searchView, name='search'),
    url(r'^$', views.index, name='index')
]

