from django import forms
from userprofile.models import *
import account.forms

class SignupForm(account.forms.SignupForm):
	fullname = forms.CharField(max_length=100,required=True)

	# roleChoice = ((1, 'Entrepreneur'),(2, 'Entrepreneur'),(3, 'Entrepreneur'))
	role = forms.ModelChoiceField(queryset=UserRole.objects.all(),required=True, empty_label=None)
	# role = forms.ChoiceField(choices=roleChoice)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['fullname','role','goal','country','state']

class GoalForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['goal']

class InvestorForm(forms.ModelForm):
	category = forms.ModelMultipleChoiceField(queryset=bizCategory.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)
	class Meta:
		model = InvestorProfile
		fields = ['category','iType','description','capital','preMoney_min','preMoney_max','expectedReturn','revenueStage_min','revenueStage_max','investAmount_min','investAmount_max']
		

class cpSeekFundForm(forms.ModelForm):
	category = forms.ModelMultipleChoiceField(queryset=bizCategory.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)
	class Meta:
		model = CompanyProfile_seekFund
		fields = ['category','description','capitalInvest','revenue','curNet','yearEstablished','employees','contactName','contactEmail','phone_number','website']

class cpSaleForm(forms.ModelForm):
	category = forms.ModelMultipleChoiceField(queryset=bizCategory.objects.all(),widget=forms.CheckboxSelectMultiple(),required=True)
	class Meta:
		model = CompanyProfile_sale
		fields = ['category','description','revenue','sales','profit','yearEstablished','employees','price','contactName','contactEmail','phone_number','website']

class FileForm(forms.ModelForm):
	class Meta:
		model = CompanyFile
		fields = ['caption','file']
			