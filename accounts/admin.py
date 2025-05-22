from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering         = ("-date_joined",)
    list_display     = ("email", "role", "is_active", "is_staff", "date_joined")
    list_filter      = ("role", "is_active", "is_staff")
    search_fields    = ("email", "first_name", "last_name")
    readonly_fields  = ("created_at", "updated_at", "last_login", "date_joined")

    fieldsets = (
        (None,                {"fields": ("email", "password")}),
        ("Personal info",     {"fields": ("first_name", "last_name")}),
        ("Roles / status",    {"fields": ("role", "is_staff", "is_superuser", "is_active")}),
        ("Important dates",   {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
        ("Permissions",       {"fields": ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_staff", "is_superuser", "is_active"),
        }),
    )
    filter_horizontal = ("groups", "user_permissions")

