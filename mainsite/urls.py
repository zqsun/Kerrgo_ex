from django.conf.urls import include,url
# from . import views
from . import views

urlpatterns = [
	#url(r'^search/?$', views.MySearchView.as_view(), name='mysearch'),
	url(r'^search/?$', views.my_basic_search, name="mysearch"),
	# url(r'^search/', include('haystack.urls')),
	url(r'^viewcompany/(?P<user_id>[0-9]+)/$',views.viewCompany, name='viewCompany'),
	url(r'^investor/(?P<user_id>[0-9]+)/$',views.viewInvestor, name='viewInvestor'),
	url(r'^investors/(?P<type_name>[\w|\W]+)/$',views.browseInvestor, name='browseInvestor'),
	url(r'^companies/(?P<goal_name>[\w|\W]+)/$',views.browseCompany, name='browseCompany'),
	url(r'^dashboard/?$', views.dashboard, name="dashboard"),
	url(r'^dashboard_investor/?$', views.dashboard_investor, name="dashboard_investor"),
	url(r'^editprofile/?$', views.editProfile_company, name="editProfile_company"),
	url(r'^editprofile_investor/?$', views.editProfile_investor, name="editProfile_investor"),
	url(r'^viewmyprofile/?$', views.viewMyprofile_company, name="viewmyProfile_company"),
	url(r'^viewmyprofile_investor/?$', views.viewMyprofile_investor, name="viewmyProfile_investor"),
	url(r'^goal/?$', views.goalChoose, name="goalChoose"),
]