from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.indexlogin), #start as login
    url(r'^register$', views.register),#register page
    url(r'^create$', views.createuser), #registers the user
    url(r'^dashboard/$', views.dashboard),#main page
    url(r'^dashboard/(?P<user_id>\d+)$', views.dashboard), #dashboard redirect with user.
    
    url(r'^showposter/(?P<x>\d+)$', views.showposter),# show a quote 
    url(r'^addtowish/(?P<x>\d+)$', views.addwish),# show a quote 
    url(r'^remove/(?P<x>\d+)$', views.remove),# removes a quote 
    
    url(r'^loginprocess$', views.loginprocess), #logs in the user
    url(r'^addquote$', views.addquote),# adds the quote
    url(r'^logout$', views.logout),#log out
]
