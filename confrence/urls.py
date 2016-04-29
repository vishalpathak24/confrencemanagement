from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^index/',views.index,name='user-index'),
    url(r'^home/',views.home,name='user-home'),
    
    url(r'^register/$',views.register,name='user-register'),
    url(r'^register/(?P<confrenceid>[0-9]+)/$',views.register),
    
    url(r'^confrence_home/$',views.confrence_home,name='confrence-home'),
    url(r'^confrence_home/(?P<confrenceid>[0-9]+)/$',views.confrence_home),
    
    url(r'^confrence_edit/$',views.confrence_edit,name='confrence-edit'),
    url(r'^confrence_edit/(?P<confrenceid>[0-9]+)/$',views.confrence_edit),
    url(r'^confrence_edit/editReviewr/$',views.reviewr_edit,name='reviewr-edit'),
    url(r'^confrence_edit/editReviewr/(?P<confrenceid>[0-9]+)/$',views.reviewr_edit), 
    url(r'^confrence_edit/editReviewr/(?P<confrenceid>[0-9]+)/(?P<authorid>[0-9]+)$',views.reviewr_edit),
    
    url(r'^confrence_edit/assgnReviewr/$',views.reviewr_assg,name='reviewr-assgn'),
    url(r'^confrence_edit/assgnReviewr/(?P<confrenceid>[0-9]+)/$',views.reviewr_assg),
    url(r'^confrence_edit/assgnReviewr/(?P<confrenceid>[0-9]+)/(?P<topicid>[0-9]+)',views.reviewr_assg),
   
    url(r'^confrence_edit/subUpload/$',views.submission_form,name='sub-upload'),
    url(r'^confrence_edit/subUpload/(?P<confrenceid>[0-9]+)/$',views.submission_form),
    url(r'^confrence_edit/subUpload/(?P<confrenceid>[0-9]+)/(?P<submissiontype>[0-9]+)$',views.submission_form),
    
    url(r'^confrence_edit/editGateway/$',views.gateway_edit,name='edit-gateway'),
    url(r'^confrence_edit/editGateway/(?P<confrenceid>[0-9]+)/$',views.gateway_edit),
    
    
    url(r'^submissions_home/$',views.submissions_home,name='submissions-home'),
    url(r'^submissions_home/review/$',views.submissions_review,name='submissions-review'),
    url(r'^submissions_home/review/(?P<subid>[0-9]+)/$',views.submissions_review,),
    
    url(r'^downloadsub/$',views.view_file,name='view-file'),
    url(r'^downloadsub/(?P<submissionid>[0-9]+)/$',views.view_file,name='view-file'),
    url(r'^viewsub/$',views.view_file1,name='view-file1'),
    url(r'^viewsub/(?P<confrenceid>[0-9]+)/$',views.view_file1,name='view-file1'),
    url(r'^chairadd/$',views.chair_add,name='chair-add'),
    url(r'^chairadd/(?P<confrenceid>[0-9]+)/$',views.chair_add,name='chair-add'),

    url(r'^pcchair/$',views.accept_reject,name='accept-reject'),
    url(r'^pcchair/(?P<confrenceid>[0-9]+)/$',views.accept_reject,name='chair-add'),
    url(r'^chairaction/$',views.chair_action,name='chair-action'),
    url(r'^chairaction/(?P<submissionid>[0-9]+)/$',views.chair_action,name='chair-action'),
]
