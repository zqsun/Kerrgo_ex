from django.conf.urls import include,url
# from . import views
from . import views

urlpatterns = [
	#url(r'^search/?$', views.my_basic_search, name="mysearch"),
	#url(r'^view/(?P<project_id>[0-9]+)/$',views.viewProject, name='viewProject'),
	#url(r'^browse/(?P<category_name>[\w|\W]+)/$',views.browseProject, name='browseProject'),
	#url(r'^service/(?P<goal_name>[\w|\W]+)/$',views.service, name='service'),
	url(r'^dashboard/?$', views.dashboard, name="dashboard"),
	url(r'^dashboard_investor/?$', views.dashboard_investor, name="dashboard_investor"),
	url(r'^editprofile/?$', views.editProfile_company, name="editProfile_company"),
	url(r'^editprofile_investor/?$', views.editProfile_investor, name="editProfile_investor"),
	url(r'^viewmyprofile/?$', views.viewMyprofile_company, name="viewmyProfile_company"),
	url(r'^viewmyprofile_investor/?$', views.viewMyprofile_investor, name="viewmyProfile_investor"),
	url(r'^goal/?$', views.goalChoose, name="goalChoose"),
]