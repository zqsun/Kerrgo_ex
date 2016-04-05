from __future__ import unicode_literals

from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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
	iType = models.ForeignKey(investorType,null=True,blank=True)
	category = models.ManyToManyField(bizCategory)
	description = models.TextField(default=" ",null=True,blank=True)
	capital = models.ForeignKey(capitalType,null=True,blank=True)
	preMoney_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	preMoney_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	expectedReturn = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
	revenueStage_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	revenueStage_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	investAmount_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	investAmount_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
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

class companyType(models.Model):
	cType = models.CharField(max_length=250,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.cType

class fundingType(models.Model):
	fType = models.CharField(max_length=250,unique=True)
	# desc_chs = models.CharField(max_length=250)
	def __unicode__(self):
		return self.fType

class CompanyProfile_seekFund(models.Model):
	company = models.ForeignKey(User)
	category = models.ManyToManyField(bizCategory)
	created_at = models.DateTimeField(auto_now_add=True)
	goal = models.ForeignKey(bizGoal,blank=True, null=True) #For company Only
	shortDescription = models.TextField(default=" ",null=True,blank=True,max_length=200)
	description = models.TextField(default=" ",null=True,blank=True)
	priorRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	curRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	nextRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	companyAge = models.FloatField(default=0)
	employees = models.IntegerField(default=0,null=True,blank=True)
	cType = models.ForeignKey(companyType,null=True,blank=True)
	productName = models.CharField(null=True,blank=True,max_length=250)
	productDescription = models.TextField(default=" ",null=True,blank=True)
	fType = models.ForeignKey(fundingType,null=True,blank=True)
	preMoney = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	interest = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
signals.post_save.connect(create_company,sender=CompanyProfile_seekFund)

class CompanyProfile_sale(models.Model):
	company = models.ForeignKey(User)
	category = models.ManyToManyField(bizCategory)
	created_at = models.DateTimeField(auto_now_add=True)
	goal = models.ForeignKey(bizGoal,blank=True, null=True) #For company Only
	shortDescription = models.TextField(default=" ",null=True,blank=True,max_length=200)
	description = models.TextField(default=" ",null=True,blank=True)
	sales = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	profit = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	fiscalYear = models.FloatField(default=0,null=True,blank=True)
	employees = models.IntegerField(default=0,null=True,blank=True)
	price = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	answerChoice = (
		('Y','Yes'),
		('N', 'No'),
		('ND', 'Not Disclosed'),
		)
	provideFinancing = models.CharField(max_length=2,choices=answerChoice,default='Y')
	pricipalsOnly = models.CharField(max_length=2,choices=answerChoice,default='Y')
	isFranchise = models.CharField(max_length=2,choices=answerChoice,default='Y')
	manageStay = models.CharField(max_length=2,choices=answerChoice,default='Y')
	relocatable = models.CharField(max_length=2,choices=answerChoice,default='Y')
	realEstateInclude = models.CharField(max_length=2,choices=answerChoice,default='Y')
signals.post_save.connect(create_company,sender=CompanyProfile_sale)













