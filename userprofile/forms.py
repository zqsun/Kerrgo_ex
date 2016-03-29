from django import forms
from userprofile.models import *
import account.forms

class SignupForm(account.forms.SignupForm):
	fullname = forms.CharField(max_length=100,required=True)

	# roleChoice = ((1, 'Entrepreneur'),(2, 'Entrepreneur'),(3, 'Entrepreneur'))
	role = forms.ModelChoiceField(queryset=UserRole.objects.all(),required=True, empty_label=None)
	# role = forms.ChoiceField(choices=roleChoice)

class ProfileForm(forms.ModelForm):
	category = forms.ModelMultipleChoiceField(queryset=bizCategory.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)
	class Meta:
		model = Profile
		fields = ['fullname','role','goal','category','country','state','description']

class GoalForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['goal']

class InvestorForm(forms.ModelForm):
	class Meta:
		model = InvestorProfile
		fields = ['iType','capital','preMoney_min','preMoney_max','expectedReturn','revenueStage_min','revenueStage_max','investAmount_min','investAmount_max']
		

class cpSeekFundForm(forms.ModelForm):
	class Meta:
		model = CompanyProfile_seekFund
		fields = ['shortDescription','priorRevenue','curRevenue','nextRevenue','companyAge',
		'employees', 'cType','productName','productDescription','fType','preMoney','interest']

class cpSaleForm(forms.ModelForm):
	class Meta:
		model = CompanyProfile_sale
		fields = ['shortDescription','sales','profit','fiscalYear','employees',
		'price', 'provideFinancing','pricipalsOnly','isFranchise','manageStay','relocatable','realEstateInclude']
			