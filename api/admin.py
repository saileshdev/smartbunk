from django.contrib import admin
from .models import SBUser, Payment, APIUsage

# Register your models here.
admin.site.register(SBUser)
admin.site.register(Payment)
admin.site.register(APIUsage)
