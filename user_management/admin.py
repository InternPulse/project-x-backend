from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import BLToken, Profile, User, Questionnaire

@admin.register(User)
class UserAdmin(UserAdmin):
    exclude = ('secret',)
    ordering = ("id",)
    search_fields = ("first_name", "last_name", "email")
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name","middle_name", "email", "role")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("email", "is_staff")
admin.site.register(BLToken)
admin.site.register(Profile)
admin.site.register(Questionnaire)