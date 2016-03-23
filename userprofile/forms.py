from django import forms
from userprofile.models import Profile,UserRole
import account.forms

class SignupForm(account.forms.SignupForm):
	fullname = forms.CharField(max_length=100,required=True)

	# roleChoice = ((1, 'Entrepreneur'),(2, 'Entrepreneur'),(3, 'Entrepreneur'))
	role = forms.ModelChoiceField(queryset=UserRole.objects.all(),required=True, empty_label=None)
	# role = forms.ChoiceField(choices=roleChoice)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['fullname','role','category','country','state','description']
