from django.conf.urls import include,url
# from . import views
from . import views
from django.views.generic import TemplateView

urlpatterns = [
	#url(r'^search/?$', views.MySearchView.as_view(), name='mysearch'),
	url(r'^search/?$', views.my_basic_search, name="mysearch"),
	# url(r'^search/', include('haystack.urls')),
	url(r'^viewcompany/(?P<goal>[\w|\W]+)/(?P<company_id>[0-9]+)/$',views.viewCompany, name='viewCompany'),
	url(r'^investor/(?P<user_id>[0-9]+)/$',views.viewInvestor, name='viewInvestor'),
	url(r'^investors/(?P<type_name>[\w|\W]+)/$',views.browseInvestor, name='browseInvestor'),
	url(r'^companies/(?P<goal_name>[\w|\W]+)/$',views.browseCompany, name='browseCompany'),
	url(r'^dashboard/?$', views.dashboard, name="dashboard"),
	url(r'^dashboard_investor/?$', views.dashboard_investor, name="dashboard_investor"),
	url(r'^dashboard_admin/?$', views.dashboard_admin, name="dashboard_admin"),
	url(r'^editprofile/?$', views.editProfile_company, name="editProfile_company"),
	url(r'^editprofile_investor/?$', views.editProfile_investor, name="editProfile_investor"),
	url(r'^investor_admin/(?P<investor_id>[0-9]+)/$', views.editInvestors_admin, name="editInvestors_admin"),
	url(r'^addinvestor_admin/?$', views.addInvestors_admin, name="addInvestors_admin"),
	url(r'^addcompany_admin/(?P<goal>[\w|\W]+)/$', views.addCompany_admin, name="addCompany_admin"),
	url(r'^company_admin/(?P<goal>[\w|\W]+)/(?P<company_id>[0-9]+)/$', views.editCompany_admin, name="editCompany_admin"),
	url(r'^viewmyprofile/?$', views.viewMyprofile_company, name="viewmyProfile_company"),
	url(r'^viewmyprofile_investor/?$', views.viewMyprofile_investor, name="viewmyProfile_investor"),
	url(r'^goal/?$', views.goalChoose, name="goalChoose"),
	url(r'^deletefile/(?P<goal>[\w|\W]+)/(?P<fid>[0-9]+)/$', views.deleteFile, name="deleteFile"),
	url(r'^google22cffa4b9737b2ae.html',TemplateView.as_view(template_name='mainsite/google22cffa4b9737b2ae.html'),)
]