from django.contrib import admin
from eventlogs.models import EventLog


class EventLogAdmin(admin.ModelAdmin):
    list_display = ("trigger", "triggered_at", "status", "is_test")
    list_filter = ("status", "is_test")


admin.site.register(EventLog)
