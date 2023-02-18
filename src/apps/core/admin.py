from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.core.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_trusty',)
    list_filter = ('email', 'is_staff', 'is_active', 'is_trusty',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'user_permissions')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)
