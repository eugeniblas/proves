from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^Home_Page/$', views.index, name='index'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<user>.*)/$', views.users, name='users'),
    url(r'^signup/$', views.signupView, name='signup'),
    url(r'^login/$', views.loginView, name='login'),
    url(r'^login/$', views.logoutView, name='logout')
]
