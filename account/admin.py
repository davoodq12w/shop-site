from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserChangeForm, ShopUserCreationForm


class AddressInline(admin.StackedInline):
    model = Address
    extra = 0


@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active',]
    inlines = [AddressInline]
    fieldsets = (
        (None, {'fields': ('phone', 'password',)}),
        ('personal info', {'fields': ('first_name', 'last_name',)}),
        ('permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('important dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone', 'password1', 'password2')}),
        ('personal info', {'fields': ('first_name', 'last_name',)}),
        ('permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        ('important dates', {'fields': ('date_joined', 'last_login')}),
    )
