from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages

from haystack.generic_views import SearchView

from userprofile.models import *
from userprofile.forms import ProfileForm,InvestorForm,cpSeekFundForm, cpSaleForm,GoalForm
from mainsite.forms import CompanySearchForm

# Create your views here.
@login_required
def dashboard(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:dashboard_investor'))
	#activeInvestor = Profile.objects.filter(isProfilecreated=True).filter(role=2,).order_by('-created_at').all()[:12]
	activeInvestor = Profile.objects.filter(role=2,).order_by('-created_at').all()[:12]
	context = {'activeInvestor':activeInvestor}
	return render(request,'mainsite/dashboard.html',context)

@login_required
def dashboard_investor(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:dashboard'))
	if p.category.all().count() == 0:
		interestCompany = Profile.objects.filter(role=1,).order_by('-created_at').all()[:12]
	else:
		interestCompany = Profile.objects.filter(category__in=p.category.all()).order_by('-created_at').all()[:12]
		if interestCompany.count() == 0:
			interestCompany = Profile.objects.filter(role=1,).order_by('-created_at').all()[:12]
	context = {'interestCompany':interestCompany}
	return render(request,'mainsite/dashboard_investor.html',context)
@login_required
def goalChoose(request):
	p = request.user.myprofile
	if request.method == 'POST':
		goal_form = GoalForm(request.POST, instance=p)
		if goal_form.is_valid():
			profile = goal_form.save()
			profile.save()
		return HttpResponseRedirect(reverse('mainsite:editProfile_company'))
	else:
		goal_form = GoalForm(instance=p)
	context = {'goal_form':goal_form}
	return render(request,'mainsite/goalchoose.html',context)

@login_required
def viewMyprofile_company(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:viewmyProfile_investor'))
	if p.goal is None:
		messages.error(request, "You haven't create your profile, please create it first")
		return HttpResponseRedirect('/goal/')
	if p.goal == bizGoal.objects.get(pk=1):
		cp, created = CompanyProfile_seekFund.objects.get_or_create(company=request.user)
		ftag = 1
	else:
		cp, created = CompanyProfile_sale.objects.get_or_create(company=request.user)
		ftag = 2
	context = {'profile':p,'cp':cp,'ftag':ftag}
	return render(request,'mainsite/viewmyprofile_company.html',context)

@login_required
def viewMyprofile_investor(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:viewmyProfile_company'))
	ip, created = InvestorProfile.objects.get_or_create(investor=request.user)
	if p.isProfilecreated is False:
		messages.error(request, "You haven't create your profile, please create it first")
		return HttpResponseRedirect(reverse('mainsite:editProfile_investor'))
	context = {'profile':p,'ip':ip}
	return render(request,'mainsite/viewmyprofile_investor.html',context)

@login_required
def editProfile_company(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:editProfile_investor'))
	if p.goal is None:
		return HttpResponseRedirect('/goal/')
	elif p.goal == bizGoal.objects.get(pk=1):
		cp, created = CompanyProfile_seekFund.objects.get_or_create(company=request.user)
		ftag = 1
	else:
		cp, created = CompanyProfile_sale.objects.get_or_create(company=request.user)
		ftag = 2
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=p)
		if ftag == 1:
			cp_form = cpSeekFundForm(request.POST,instance=cp)
		else:
			cp_form = cpSaleForm(request.POST,instance=cp)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.isProfilecreated = True
			profile.save()
			profile_form.save_m2m()
			messages.success(request, 'Your profile is successfullly updated.')
		if cp_form.is_valid():
			companyprofile = cp_form.save(commit=False)
			companyprofile.goal = profile.goal
			companyprofile.save()
		return HttpResponseRedirect(reverse('mainsite:dashboard'))
		#return HttpResponseRedirect(reverse('mainsite:editProfile_company')) 
	else:
		profile_form = ProfileForm(instance=p)
		if ftag == 1:
			cp_form = cpSeekFundForm(instance=cp)
		else:
			cp_form = cpSaleForm(instance=cp)
	context = {'profile_form':profile_form,'cp_form':cp_form,'ftag':ftag}
	return render(request,'mainsite/editprofile_company.html',context)

@login_required
def editProfile_investor(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:editProfile_company'))
	ip, created = InvestorProfile.objects.get_or_create(investor=request.user)
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=p)
		ip_form = InvestorForm(request.POST, instance=ip)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.isProfilecreated = True
			profile.save()
			profile_form.save_m2m()
			messages.success(request, 'Your profile is successfullly updated.')
		if ip_form.is_valid():
			new_ip = ip_form.save()
			new_ip.save()
		return HttpResponseRedirect(reverse('mainsite:dashboard_investor'))
	else:
		profile_form = ProfileForm(instance=p)
		ip_form =  InvestorForm(instance=ip)
	context = {'profile_form':profile_form,'ip_form':ip_form}
	return render(request,'mainsite/editProfile_investor.html',context)

class MySearchView(SearchView):
    """My custom search view."""
    template_name = 'search/search.html'
    #queryset = SearchQuerySet().filter(author='john')
    form_class = CompanySearchForm

    def get_queryset(self):
        queryset = super(MySearchView, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # do something
        return context

