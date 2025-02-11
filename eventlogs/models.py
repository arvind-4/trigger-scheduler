from django.db import models
from triggers.models import Trigger


class EventLog(models.Model):
    STATUS_CHOICES = (("active", "Active"), ("archived", "Archived"))

    trigger = models.ForeignKey(
        Trigger, on_delete=models.SET_NULL, null=True, blank=True
    )
    trigger_data = models.JSONField()
    triggered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    payload = models.JSONField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
    is_test = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.trigger:
            self.trigger_data = self.trigger.to_event_data()
        super().save(*args, **kwargs)
