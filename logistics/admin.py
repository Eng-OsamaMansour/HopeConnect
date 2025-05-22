from django.contrib import admin
from .models import Delivery


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display  = (
        "id", "donation", "status",
        "distance_km", "eta_min",
        "pickup_latlng", "dropoff_latlng",
        "created_at",
    )
    list_filter   = ("status", "created_at")
    search_fields = ("donation__id", "pickup_latlng", "dropoff_latlng")
    readonly_fields = ("created_at", "updated_at")

    def distance_km(self, obj):
        return round((obj.distance_m or 0) / 1000, 2)
    distance_km.short_description = "Distance (km)"

    def eta_min(self, obj):
        return round((obj.duration_s or 0) / 60)
    eta_min.short_description = "ETA (min)"
