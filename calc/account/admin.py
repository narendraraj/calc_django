from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

from django import forms
# from django.contrib import admin


from account.forms import CustomUserCreationForm, CustomUserChangeForm
# from account.forms import UserCreationForm, UserChangeForm


# Register your models here.
MyUser = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_active', 'is_staff',  'is_admin',
                    'is_superuser', 'last_login', 'date_joined')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin',
                                    'is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'password1', 'password2', ),

        }),
        ('Permissions', {'fields': ('is_active',
                                    'is_staff', 'is_admin', 'is_superuser',)}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
