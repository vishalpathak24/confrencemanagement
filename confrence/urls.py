from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^home/',views.home,name='user-home'),
    url(r'^register/',views.register,name='user-register'),
    url(r'^confrence_home/$',views.confrence_home,name='confrence-home'),
    url(r'^confrence_home/(?P<confrenceid>[0-9]+)/$',views.confrence_home),
    url(r'^confrence_edit/$',views.confrence_edit,name='confrence-edit'),
    url(r'^confrence_edit/(?P<confrenceid>[0-9]+)/$',views.confrence_edit),
    url(r'^confrence_edit/editReviewr/$',views.reviewr_edit,name='reviewr-edit'),
    url(r'^confrence_edit/editReviewr/(?P<confrenceid>[0-9]+)/$',views.reviewr_edit), 
    url(r'^confrence_edit/editReviewr/(?P<confrenceid>[0-9]+)/(?P<authorid>[0-9]+)$',views.reviewr_edit),
    url(r'^confrence_edit/subUpload/$',views.submission_form,name='sub-upload'),
    url(r'^confrence_edit/subUpload/(?P<confrenceid>[0-9]+)/(?P<submissiontype>[0-9]+)$',views.submission_form),
    url(r'^viewsub/$',views.view_file,name='view-file'),
    url(r'^viewsub/(?P<submissionid>[0-9]+)/$',views.view_file,name='view-file'),
    url(r'^viewtest/$',views.view_file1,name='view-file1'),
    url(r'^viewtest/(?P<confrenceid>[0-9]+)/$',views.view_file1,name='view-file1')
]
