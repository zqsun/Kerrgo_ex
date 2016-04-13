import os
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms import formset_factory
from django.shortcuts import get_object_or_404

from django.contrib.contenttypes.models import ContentType

from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet,EmptySearchQuerySet

from userprofile.models import *
from userprofile.forms import ProfileForm,InvestorForm,cpSeekFundForm, cpSaleForm,GoalForm
from mainsite.forms import CompanySearchForm

# Create your views here.
@login_required
def dashboard(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:dashboard_investor'))
	if p.role == UserRole.objects.get(pk=4):
		return HttpResponseRedirect(reverse('mainsite:dashboard_admin'))
	#activeInvestor = Profile.objects.filter(isProfilecreated=True).filter(role=2,).order_by('-created_at').all()[:12]
	activeInvestor = Profile.objects.filter(role=2,).order_by('-created_at').all()[:12]
	context = {'activeInvestor':activeInvestor}
	return render(request,'mainsite/dashboard.html',context)

@login_required
def dashboard_investor(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:dashboard'))
	if p.role == UserRole.objects.get(pk=4):
		return HttpResponseRedirect(reverse('mainsite:dashboard_admin'))
	interestCompany = CompanyProfile.objects.all().order_by('-created_at').all()[:12]
	# interestCompany = Profile.objects.filter(role=1,).order_by('-created_at').all()[:12]
	# if p.category.all().count() == 0:
	# 	interestCompany = Profile.objects.filter(role=1,).order_by('-created_at').all()[:12]
	# else:
	# 	interestCompany = Profile.objects.filter(category__in=p.category.all()).order_by('-created_at').all()[:12]
	# 	if interestCompany.count() == 0:
	# 		interestCompany = Profile.objects.filter(role=1,).order_by('-created_at').all()[:12]
	context = {'interestCompany':interestCompany}
	return render(request,'mainsite/dashboard_investor.html',context)

@login_required
def dashboard_admin(request):
	p = request.user.myprofile
	investors = InvestorProfile.objects.filter(investor=request.user)
	companySale = CompanyProfile_sale.objects.filter(company=request.user)
	companySeek = CompanyProfile_seekFund.objects.filter(company=request.user)
	context = {'investors':investors, 'companySale':companySale,'companySeek':companySeek}
	return render(request,'mainsite/dashboard_admin.html',context)

@login_required
def editInvestors_admin(request,investor_id):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:editProfile_company'))
	ip = InvestorProfile.objects.get(pk=investor_id)
	if request.method == 'POST':
		ip_form = InvestorForm(request.POST, instance=ip)
		if ip_form.is_valid():
			new_ip = ip_form.save(commit=False)
			new_ip.investor = request.user
			new_ip.save()
			ip_form.save_m2m()
			messages.success(request, "Investor's profile is successfullly updated.")
			#ip_form.save_m2m()
		return HttpResponseRedirect(reverse('mainsite:dashboard_admin'))
	else:
		ip_form =  InvestorForm(instance=ip)
	context = {'ip_form':ip_form,'tflag':"edit",'investor_id':investor_id}
	return render(request,'mainsite/editInvestors_admin.html',context)

@login_required
def addInvestors_admin(request):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=1):
		return HttpResponseRedirect(reverse('mainsite:editProfile_company'))
	# ip = InvestorProfile.objects.get(pk=investor_id)
	if request.method == 'POST':
		ip_form = InvestorForm(request.POST)
		if ip_form.is_valid():
			new_ip = ip_form.save(commit=False)
			new_ip.investor = request.user
			new_ip.save()
			ip_form.save_m2m()
			messages.success(request, "Investor's profile is successfullly updated.")
			#ip_form.save_m2m()
		return HttpResponseRedirect(reverse('mainsite:dashboard_investor'))
	else:
		ip_form =  InvestorForm()
	context = {'ip_form':ip_form}
	return render(request,'mainsite/editInvestors_admin.html',context)

@login_required
def  addCompany_admin(request,goal):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:editProfile_investor'))
	
	if goal == "seek":
		ftag = 1
	else:
		# cp, created = CompanyProfile_sale.objects.get_or_create(company=request.user)
		ftag = 2
	#filesFormSet = formset_factory()
	#cp.name = p.fullname
	if request.method == 'POST':
		if ftag == 1:
			cp_form = cpSeekFundForm(request.POST)
		else:
			cp_form = cpSaleForm(request.POST)
			#profile_form.save_m2m()
		if cp_form.is_valid():
			companyprofile = cp_form.save(commit=False)
			companyprofile.goal = bizGoal.objects.get(pk=ftag)
			companyprofile.company = request.user
			companyprofile.save()
			cp_form.save_m2m()
			for afile in request.FILES.getlist('documents'):
				if ftag == 1:
					cf = CompanyFile_seek()
				else:
					cf = CompanyFile_sale()
				cf.companyprofile = companyprofile
				cf.file = afile
				cf.save()
			messages.success(request, 'Your profile is successfullly updated.')
		return HttpResponseRedirect(reverse('mainsite:dashboard_admin'))
		#return HttpResponseRedirect(reverse('mainsite:editProfile_company')) 
	else:
		if ftag == 1:
			cp_form = cpSeekFundForm()
		else:
			cp_form = cpSaleForm()
	isAdd = True
	context = {'cp_form':cp_form,'ftag':ftag,'isAdd':isAdd}
	return render(request,'mainsite/editcompany_admin.html',context)

@login_required
def editCompany_admin(request,goal,company_id):
	p = request.user.myprofile
	if p.role == UserRole.objects.get(pk=2):
		return HttpResponseRedirect(reverse('mainsite:editProfile_investor'))
	if goal == 'seek':
		cp = CompanyProfile_seekFund.objects.get(pk=company_id)
		ftag = 1
	else:
		cp = CompanyProfile_sale.objects.get(pk=company_id)
		ftag = 2
	print ftag
	if request.method == 'POST':
		if ftag == 1:
			cp_form = cpSeekFundForm(request.POST,instance=cp)
		else:
			cp_form = cpSaleForm(request.POST,instance=cp)	
		if cp_form.is_valid():
			companyprofile = cp_form.save(commit=False)
			companyprofile.goal = bizGoal.objects.get(pk=ftag)
			companyprofile.company = request.user
			companyprofile.save()
			cp_form.save_m2m()
			for afile in request.FILES.getlist('documents'):
				if ftag == 1:
					cf = CompanyFile_seek()
				else:
					cf = CompanyFile_sale()
				cf.companyprofile = companyprofile
				cf.file = afile
				cf.save()
			# gcp = CompanyProfile(content_object=companyprofile,created_at=companyprofile.created_at)
			# gcp.save()
			messages.success(request, 'Your profile is successfullly updated.')
		return HttpResponseRedirect(reverse('mainsite:dashboard_admin')) 
	else:
		if ftag == 1:
			cp_form = cpSeekFundForm(instance=cp)
			documents = CompanyFile_seek.objects.filter(companyprofile=cp)
		else:
			cp_form = cpSaleForm(instance=cp)
			documents = CompanyFile_sale.objects.filter(companyprofile=cp)
	isAdd = False
	context = {'cp_form':cp_form,'ftag':ftag,'isAdd':isAdd,'company_id':company_id,'documents':documents}
	return render(request,'mainsite/editcompany_admin.html',context)


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
		documents = CompanyFile_seek.objects.filter(companyprofile=cp)
		ftag = 1
	else:
		cp, created = CompanyProfile_sale.objects.get_or_create(company=request.user)
		documents = CompanyFile_sale.objects.filter(companyprofile=cp)
		ftag = 2
	context = {'profile':p,'cp':cp,'ftag':ftag,'documents':documents}
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
	#filesFormSet = formset_factory()
	cp.name = p.fullname
	if request.method == 'POST':
		profile_form = ProfileForm(request.POST, instance=p)
		#fileform = FileForm(request.POST,request.FILE)
		#ffs = filesFormSet(request.POST,request.FILE)
		if ftag == 1:
			cp_form = cpSeekFundForm(request.POST,instance=cp)
		else:
			cp_form = cpSaleForm(request.POST,instance=cp)
		if profile_form.is_valid():
			profile = profile_form.save(commit=False)
			profile.isProfilecreated = True
			profile.save()
			p = profile
			#profile_form.save_m2m()
			messages.success(request, 'Your profile is successfullly updated.')
		if cp_form.is_valid():
			companyprofile = cp_form.save(commit=False)
			companyprofile.goal = p.goal
			companyprofile.created_at = p.created_at
			companyprofile.name = p.fullname
			companyprofile.country = p.country
			companyprofile.state = p.state
			companyprofile.save()
			cp_form.save_m2m()
			for afile in request.FILES.getlist('documents'):
				if ftag == 1:
					cf = CompanyFile_seek()
				else:
					cf = CompanyFile_sale()
				cf.companyprofile = companyprofile
				cf.file = afile
				cf.save()
		return HttpResponseRedirect(reverse('mainsite:dashboard'))
		#return HttpResponseRedirect(reverse('mainsite:editProfile_company')) 
	else:
		profile_form = ProfileForm(instance=p)
		if ftag == 1:
			cp_form = cpSeekFundForm(instance=cp)
			documents = CompanyFile_seek.objects.filter(companyprofile=cp)
		else:
			cp_form = cpSaleForm(instance=cp)
			documents = CompanyFile_sale.objects.filter(companyprofile=cp)
	context = {'profile_form':profile_form,'cp_form':cp_form,'ftag':ftag,'documents':documents}
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
			p = profile
			#profile_form.save_m2m()
			messages.success(request, 'Your profile is successfullly updated.')
		if ip_form.is_valid():
			new_ip = ip_form.save(commit=False)
			new_ip.name = p.fullname
			new_ip.country = p.country
			new_ip.state = p.state
			new_ip.save()
			ip_form.save_m2m()
		return HttpResponseRedirect(reverse('mainsite:dashboard_investor'))
	else:
		profile_form = ProfileForm(instance=p)
		ip_form =  InvestorForm(instance=ip)
	context = {'profile_form':profile_form,'ip_form':ip_form}
	return render(request,'mainsite/editProfile_investor.html',context)

@login_required
def viewCompany(request,goal,company_id):
	#p = Profile.objects.get(user=user_id)
	if goal == 'seek':
		cp = CompanyProfile_seekFund.objects.get(pk=company_id)
		documents = CompanyFile_seek.objects.filter(companyprofile=cp)
		ftag = 1
	else:
		cp = CompanyProfile_sale.objects.get(pk=company_id)
		documents = CompanyFile_sale.objects.filter(companyprofile=cp)
		ftag = 2
	context = {'cp':cp,'ftag':ftag,'documents':documents}
	return render(request,'mainsite/viewmyprofile_company.html',context)

@login_required
def viewInvestor(request,user_id):
	p = Profile.objects.get(user=user_id)
	ip = InvestorProfile.objects.get(investor=user_id)
	context = {'profile':p,'ip':ip}
	return render(request,'mainsite/viewmyprofile_investor.html',context)

def browseInvestor(request,type_name):
    if type_name == "ALL":
        results = InvestorProfile.objects.all().order_by('-created_at')
    else:
        results = InvestorProfile.objects.filter(iType__iType__contains=type_name).order_by('-created_at')
    #company_form = CompanySearchForm()
    context = {'results':results,'type':type_name}
    return render(request, 'mainsite/browseInvestor.html', context)

def browseCompany(request,goal_name):
	if goal_name == "all":
		results = CompanyProfile.objects.all().order_by('-created_at')
	elif goal_name == "seek":
		results = CompanyProfile_seekFund.objects.all()
		goal = "Seeking Funding"
	else:
		results = CompanyProfile_sale.objects.all()
		goal = "Selling Company"
	company_form = CompanySearchForm()
	context = {'results':results,'goal':goal_name,'form':company_form}
	return render(request, 'mainsite/browseCompany.html', context)

def my_basic_search(request, template='search/search.html', load_all=True, form_class=CompanySearchForm, searchqueryset=None, extra_context=None, results_per_page=None):
    """
    A more traditional view that also demonstrate an alternative
    way to use Haystack.
    Useful as an example of for basing heavily custom views off of.
    Also has the benefit of thread-safety, which the ``SearchView`` class may
    not be.
    Template:: ``search/search.html``
    Context::
        * form
          An instance of the ``form_class``. (default: ``ModelSearchForm``)
        * page
          The current page of search results.
        * paginator
          A paginator instance for the results.
        * query
          The query received by the form.
    """
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    #paginator = Paginator(results, results_per_page or RESULTS_PER_PAGE)

    # try:
    #     page = paginator.page(int(request.GET.get('page', 1)))
    # except InvalidPage:
    #     raise Http404("No such page of results!")

    context = {
        'form': form,
        #'page': page,
        #'paginator': paginator,
        'results':results,
        'query': query,
        'suggestion': None,
    }

    if results.query.backend.include_spelling:
        context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render(request, template, context)

@login_required
def deleteFile(request,goal,fid):
	if goal == "seek":
		cf = get_object_or_404(CompanyFile_seek,pk=fid)
	else:
		cf = get_object_or_404(CompanyFile_sale,pk=fid)
	name = os.path.basename(cf.file.name)
	cf.delete()
	q = request.GET.get('q', '')
	messages.success(request, '%s is successfullly deleted.' % name)
	return HttpResponseRedirect(q)




