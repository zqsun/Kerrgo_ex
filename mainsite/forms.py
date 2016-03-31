from django import forms
from haystack.forms import SearchForm
from userprofile.models import bizCategory, bizGoal

class CompanySearchForm(SearchForm):
	category = forms.ModelChoiceField(queryset=bizCategory.objects.all(),required=False,empty_label="All Categories")
	goal = forms.ModelChoiceField(queryset=bizGoal.objects.all(),required=False,empty_label="All Goal")
	def serch(self):
		sqs = super(CompanySearchForm, self).search()
		if not self.is_valid():
			return self.no_query_found()
		# return self.no_query_found()

		if self.cleaned_data['category']:
			sqs = sqs.filter(category=self.cleaned_data['category'])
		if self.cleaned_data['goal']:
			sqs = sqs.filter(goal=bizGoal.objects.get(pk=self.cleaned_data['goal']))
		# sqs = None
		return sqs