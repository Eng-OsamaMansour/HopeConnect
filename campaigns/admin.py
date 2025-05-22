from django.contrib import admin
from .models import Campaign, CampaignCategory


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display   = (
        "title", "category", "goal_amount",
        "start", "end", "is_open", "created_at",
    )
    list_filter    = ("category", "is_open", "start")
    search_fields  = ("title",)
    readonly_fields = ("created_at",)
    ordering       = ("-start",)

    fieldsets = (
        (None, {"fields": ("title", "category", "goal_amount")}),
        ("Timeline", {"fields": ("start", "end", "is_open")}),
        ("System",   {"fields": ("created_at",)}),
    )
