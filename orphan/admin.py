from django.contrib import admin

from .models import Orphan, OrphanUpdate

@admin.register(Orphan)
class OrphanAdmin(admin.ModelAdmin):
    list_display = ('name', 'orphanage', 'gender', 'birth_date', 'age')
    list_filter = ('orphanage', 'gender')
    search_fields = ('name', 'orphanage__name')
    readonly_fields = ('age',)

@admin.register(OrphanUpdate)
class OrphanUpdateAdmin(admin.ModelAdmin):
    list_display = ('orphan', 'title', 'created_at')
    list_filter = ('orphan__orphanage', 'created_at')
    search_fields = ('title', 'note', 'orphan__name')
    date_hierarchy = 'created_at'

