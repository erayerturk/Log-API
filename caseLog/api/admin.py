from django.contrib import admin

from api.models import Company, Log, CustomUser

admin.site.register(Company)
admin.site.register(Log)
admin.site.register(CustomUser)
