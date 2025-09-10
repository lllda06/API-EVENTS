from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'meeting_time', 'description')
    list_filter = ('meeting_time',)
    search_fields = ('name', 'description')