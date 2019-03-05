from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.success),
    url(r'^logout$', views.logout),
    url(r'^submit$', views.submit),
    url(r'^trips/new$', views.createtrip),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^trips/(?P<id>\d+)$', views.show),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^cancel/(?P<id>\d+)$', views.cancel),
]
