from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUserProfile

# Register your models here.
# admin.site.register(CustomUserProfile)
@admin.register(CustomUserProfile)
class CustomUserAdmin(BaseUserAdmin):
    """ Custom user admin."""

    fieldsets = (
        (None, {'fields': ('password',)}),
                (_('Personal info'), {'fields': ('email', 'first_name', 'last_name', 'photo' )}),
                (_('Permissions'), {
                    'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2',)
        }),
    )

    # exclude = ['__all__']
    ordering = ['email', 'first_name', 'last_name']
    list_display = ['email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    filter_horizontal = ('groups', 'user_permissions',)
