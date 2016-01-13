from django.conf.urls import url

from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.posts_index, name="index"),
    url(r'^create$', views.posts_create, name="create"),
    url(r'^(?P<id>\d+)/$', views.posts_show, name="show"),
    url(r'^(?P<id>\d+)/edit/$', views.posts_update, name="edit"),
    url(r'^(?P<id>\d+)/delete/$', views.posts_delete, name="delete"),
]