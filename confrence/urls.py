from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^home/',views.home,name='user-home'),
    url(r'^register/',views.register,name='user-register'),
]
