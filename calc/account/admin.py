from tokenize import group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.models import Group

# from django.contrib import admin


from account.forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import ugettext, ugettext_lazy as _

# from account.forms import UserCreationForm, UserChangeForm


# Register your models here.
MyUser = get_user_model()


class CustomUserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "email",
        "is_active",
        "is_staff",
        "is_admin",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    list_filter = ("is_admin",)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = (
                "is_active",
                "is_staff",
                "is_admin",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ("is_active", "is_staff", "groups")

        return [
            (
                None,
                {
                    "fields": (
                        "email",
                        "password",
                    )
                },
            ),
            (
                _("Personal info"),
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
            (_("Permissions"), {"fields": perm_fields}),
            (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        ]

    # fieldsets = (
    #     (None, {'fields': ('email', 'password',)}),
    #     ('Personal info', {'fields': ()}),
    #     ('Permissions', {'fields': ('is_active', 'is_staff',
    #                                 'is_superuser', 'groups', 'user_permissions', )}),
    # )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                )
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj and obj.id == request.user.id)


# Now register the new UserAdmin...

admin.site.register(MyUser, CustomUserAdmin)
admin.site.unregister(Group)
