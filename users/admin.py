from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext as _

from users.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields":
                (
                    "username",
                    "first_name",
                    "last_name"
                )
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            _("Important dates"),
            {"fields": ("bio", "avatar", "follower")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "bio", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "bio", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
