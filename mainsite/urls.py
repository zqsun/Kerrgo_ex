from django.conf.urls import include,url
# from . import views
from . import views

urlpatterns = [
	#url(r'^search/?$', views.my_basic_search, name="mysearch"),
	#url(r'^view/(?P<project_id>[0-9]+)/$',views.viewProject, name='viewProject'),
	#url(r'^browse/(?P<category_name>[\w|\W]+)/$',views.browseProject, name='browseProject'),
	#url(r'^service/(?P<goal_name>[\w|\W]+)/$',views.service, name='service'),
	url(r'^dashboard/?$', views.dashboard, name="dashboard"),
]