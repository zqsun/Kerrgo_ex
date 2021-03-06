from __future__ import unicode_literals

import os
from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.validators import RegexValidator
from django.dispatch import receiver

# Create your models here.

class UserRole(models.Model):
	role = models.CharField(max_length=100,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.role

class bizCategory(models.Model):
	category = models.CharField(max_length=250,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.category

class bizGoal(models.Model):
	goal = models.CharField(max_length=250,unique=True)
	def __unicode__(self):
		return self.goal

class Profile(models.Model):
	user = models.OneToOneField(User,related_name='myprofile')
	fullname = models.CharField(max_length=100)
	#company = models.CharField(max_length=150,null=True,blank=True)
	#description = models.TextField(default=" ",null=True,blank=True)
	#logo = models.ImageField(upload_to='profile_images',blank=True)
	role = models.ForeignKey(UserRole)
	# category = models.ManyToManyField(bizCategory)
	goal = models.ForeignKey(bizGoal,blank=True, null=True) #For company Only
	# Location
	country = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	#description = models.TextField(default=" ",null=True,blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	isProfilecreated = models.BooleanField(default=False)
	# address = models.CharField(max_length=150)
	def __unicode__(self):
		return self.user

# Investor Profile
class investorType(models.Model):
	iType = models.CharField(max_length=250,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.iType

class capitalType(models.Model):
	capital = models.CharField(max_length=250,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.capital

class InvestorProfile(models.Model):
	investor = models.ForeignKey(User)
	name = models.CharField(max_length=100,null=True,blank=True)
	iType = models.ForeignKey(investorType,null=True,blank=True)
	category = models.ManyToManyField(bizCategory)
	created_at = models.DateTimeField(auto_now_add=True)
	description = models.TextField(default=" ",null=True,blank=True)
	capital = models.ForeignKey(capitalType,null=True,blank=True)
	preMoney_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	preMoney_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	expectedReturn = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
	revenueStage_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	revenueStage_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	investAmount_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	investAmount_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	country = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	def __unicode__(self):
		return self.user

# Company Profile

class CompanyProfile(models.Model):
 	content_type = models.ForeignKey(ContentType)
 	object_id = models.PositiveIntegerField()
 	content_object = GenericForeignKey('content_type','object_id')
 	created_at = models.DateTimeField(auto_now_add=True)
 	# def __str__(self):
 	# 	return self.content_object.company.myprofile.fullname
def create_company(sender,instance,created, **kwargs):
 	content_type = ContentType.objects.get_for_model(instance)
 	company,_created = CompanyProfile.objects.get_or_create(content_type=content_type,object_id=instance.id)
 	company.created_at = instance.created_at
 	company.save()

# class companyType(models.Model):
# 	cType = models.CharField(max_length=250,unique=True)
# 	# desc_chs = models.CharField(max_length=250)
# 	def __unicode__(self):
# 		return self.cType

# class fundingType(models.Model):
# 	fType = models.CharField(max_length=250,unique=True)
# 	# desc_chs = models.CharField(max_length=250)
# 	def __unicode__(self):
# 		return self.fType

class CompanyProfile_seekFund(models.Model):
	company = models.ForeignKey(User)
	name = models.CharField(max_length=100,null=True,blank=True)
	category = models.ManyToManyField(bizCategory)
	created_at = models.DateTimeField(auto_now_add=True)
	goal = models.ForeignKey(bizGoal,blank=True, null=True) #For company Only
	description = models.TextField(default=" ",null=True,blank=True)
	capitalInvest = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	revenueChoice = (
		('Y','Yes'),
		('N', 'No'),
		)
	revenue = models.CharField(max_length=2,choices=revenueChoice,default='N')
	curNet = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	yearEstablished = models.IntegerField(default=0,null=True,blank=True)
	employees = models.IntegerField(default=0,null=True,blank=True)
	# files = GenericRelation(CompanyFile)
	# Contact
	contactName = models.CharField(max_length=100,default=" ",null=True,blank=True)
	contactEmail = models.EmailField(max_length=254,default=" ",null=True,blank=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True,null=True,max_length=15) # validators should be a list
	website = models.URLField(blank=True,null=True)
	country = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	# priorRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	# curRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	# nextRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	# companyAge = models.FloatField(default=0)
	# employees = models.IntegerField(default=0,null=True,blank=True)
	# cType = models.ForeignKey(companyType,null=True,blank=True)
	# productName = models.CharField(null=True,blank=True,max_length=250)
	# productDescription = models.TextField(default=" ",null=True,blank=True)
	# fType = models.ForeignKey(fundingType,null=True,blank=True)
	# preMoney = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	# interest = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
signals.post_save.connect(create_company,sender=CompanyProfile_seekFund)

class CompanyProfile_sale(models.Model):
	company = models.ForeignKey(User)
	name = models.CharField(max_length=100,null=True,blank=True)
	category = models.ManyToManyField(bizCategory)
	created_at = models.DateTimeField(auto_now_add=True)
	goal = models.ForeignKey(bizGoal,blank=True, null=True) #For company Only
	description = models.TextField(default=" ",null=True,blank=True)
	revenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	sales = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	profit = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	yearEstablished = models.IntegerField(default=0,null=True,blank=True)
	employees = models.IntegerField(default=0,null=True,blank=True)
	price = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	# files = GenericRelation(CompanyFile)
	# Contact
	contactName = models.CharField(max_length=100,default=" ",null=True,blank=True)
	contactEmail = models.EmailField(max_length=254,default=" ",null=True,blank=True)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True,null=True,max_length=15) # validators should be a list
	website = models.URLField(blank=True,null=True)
	country = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)

	# answerChoice = (
	# 	('Y','Yes'),
	# 	('N', 'No'),
	# 	('ND', 'Not Disclosed'),
	# 	)
	# provideFinancing = models.CharField(max_length=2,choices=answerChoice,default='Y')
	# pricipalsOnly = models.CharField(max_length=2,choices=answerChoice,default='Y')
	# isFranchise = models.CharField(max_length=2,choices=answerChoice,default='Y')
	# manageStay = models.CharField(max_length=2,choices=answerChoice,default='Y')
	# relocatable = models.CharField(max_length=2,choices=answerChoice,default='Y')
	# realEstateInclude = models.CharField(max_length=2,choices=answerChoice,default='Y')
signals.post_save.connect(create_company,sender=CompanyProfile_sale)

def user_diretory_path(instance,filename):
	return 'user_{0}/{1}/{2}'.format(instance.companyprofile.id,uuid4().hex,filename)

class CompanyFile_sale(models.Model):
	# caption = models.CharField(max_length=100,null=True,default='Company Document',blank=True)
	companyprofile = models.ForeignKey(CompanyProfile_sale)
	file = models.FileField(upload_to=user_diretory_path,null=True,blank=True)
	
	# object_id = models.PositiveIntegerField()
	# content_object = GenericForeignKey('content_type','content_object')

class CompanyFile_seek(models.Model):
	# caption = models.CharField(max_length=100,null=True,default='Company Document',blank=True)
	companyprofile = models.ForeignKey(CompanyProfile_seekFund)
	file = models.FileField(upload_to=user_diretory_path,null=True,blank=True)

@receiver(models.signals.post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    list_of_models = ('CompanyFile_sale','CompanyFile_seek')
    if sender.__name__ in list_of_models:
		if instance.file:
			if os.path.isfile(instance.file.path):
				dirname = os.path.dirname(instance.file.path)
				os.remove(instance.file.path)
				os.rmdir(dirname)











