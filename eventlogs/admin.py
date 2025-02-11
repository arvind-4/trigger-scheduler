from django.contrib import admin

# Register your models here.

from eventlogs.models import EventLog

# trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)
#     triggered_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
#     payload = models.JSONField(null=True, blank=True)
#     response = models.JSONField(null=True, blank=True)
#     is_test = models.BooleanField(default=False)
#     error = models.TextField(null=True, blank=True)


class EventLogAdmin(admin.ModelAdmin):
    list_display = ('trigger', 'triggered_at', 'status', 'is_test')
    list_filter = ('status', 'is_test')

admin.site.register(EventLog)