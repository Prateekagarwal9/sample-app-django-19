from django.conf.urls import url

from . import views

app_name = 'posts'
urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^create$', views.create, name="create"),
    url(r'^(?P<slug>[-\w]+)/$', views.show, name="show"),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.update, name="edit"),
    url(r'^(?P<slug>[-\w]+)/delete/$', views.delete, name="delete"),
]