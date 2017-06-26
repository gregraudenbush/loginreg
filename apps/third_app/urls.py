from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^val$', views.val),
    url(r'^login$', views.login),
    url(r'^newuser$', views.newuser)
]