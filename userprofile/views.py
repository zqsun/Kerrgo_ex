from django.shortcuts import render

import account.views
from userprofile.forms import SignupForm

from django.dispatch import receiver
from django.db.models.signals import post_save
from userprofile.models import Profile,UserRole,InvestorProfile

from django.contrib.auth.models import User

# Create your views here.

@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,role=UserRole.objects.get(pk=1))

class SignupView(account.views.SignupView):

	form_class = SignupForm

	def after_signup(self, form):
		self.create_profile(form)
		super(SignupView, self).after_signup(form)

	def create_profile(self, form):
		profile = self.created_user.myprofile
		profile.fullname = form.cleaned_data["fullname"]
		profile.role = form.cleaned_data["role"]
		# profile.role = UserRole.objects.get(pk=form.cleaned_data["role"])
		if profile.role == UserRole.objects.get(pk=2):
			InvestorProfile.objects.create(investor=profile.user)
		profile.save()


