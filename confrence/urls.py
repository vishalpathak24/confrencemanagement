from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^home/',views.home,name='user-home'),
    url(r'^register/',views.register,name='user-register'),
    url(r'^confrence_home/$',views.confrence_home,name='confrence-home'),
    url(r'^confrence_home/(?P<confrenceid>[0-9]+)/$',views.confrence_home),
    url(r'^confrence_edit/$',views.confrence_edit,name='confrence-edit'),
    url(r'^confrence_edit/(?P<confrenceid>[0-9]+)/$',views.confrence_edit,),
]
