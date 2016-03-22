from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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

class Profile(models.Model):
	user = models.OneToOneField(User,related_name='myprofile')
	fullname = models.CharField(max_length=100,null=True,blank=True)
	#company = models.CharField(max_length=150,null=True,blank=True)
	#description = models.TextField(default=" ",null=True,blank=True)
	#logo = models.ImageField(upload_to='profile_images',blank=True)
	role = models.ForeignKey(UserRole)
	category = models.ManyToManyField(bizCategory)
	# Location
	country = models.CharField(max_length=100,null=True,blank=True)
	state = models.CharField(max_length=100,null=True,blank=True)
	description = models.TextField(default=" ",null=True,blank=True)
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
	iType = models.ForeignKey(investorType)
	capital = models.ForeignKey(capitalType)
	preMoney_min = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	preMoney_max = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	expectedReturn = models.DecimalField(default=0,max_digits=4,decimal_places=2,null=True,blank=True)
	investAmount = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	def __unicode__(self):
		return self.user

# Company Profile

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

class CompanyProfile(models.Model):
	company = models.ForeignKey(User)
	shortDescription = models.TextField(default=" ",null=True,blank=True,max_length=200)
	priorRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	curRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	nextRevenue = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	companyAge = models.FloatField(default=0)
	employees = models.IntegerField(default=0,null=True,blank=True)
	cType = models.ForeignKey(companyType)
	productName = models.CharField(null=True,blank=True,max_length=250)
	productDescription = models.TextField(default=" ",null=True,blank=True)
	fType = models.ForeignKey(fundingType)
	preMoney = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)
	interest = models.DecimalField(max_digits=11,decimal_places=2,default=0,null=True,blank=True)














