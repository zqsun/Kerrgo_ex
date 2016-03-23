from django.contrib import admin
#from userprofile.models import UserRole, bizCategory, Profile,investorType, capitalType, InvestorProfile, companyType,fundingType, CompanyProfile
from userprofile.models import *
# Register your models here.
admin.site.register(UserRole)
admin.site.register(bizCategory)
admin.site.register(Profile)
admin.site.register(investorType)
admin.site.register(capitalType)
admin.site.register(InvestorProfile)
admin.site.register(companyType)
admin.site.register(fundingType)
admin.site.register(CompanyProfile)
