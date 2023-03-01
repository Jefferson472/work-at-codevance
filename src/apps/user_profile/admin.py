from django.contrib import admin

from apps.user_profile.models import Supplier, Operator


admin.site.register(Supplier)
admin.site.register(Operator)
