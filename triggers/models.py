from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Trigger(models.Model):
    TRIGGER_TYPES = (
        ('scheduled', 'Scheduled'),
        ('api', 'API')
    )
    
    INTERVAL_TYPES = (
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('fixed_time', 'Fixed Time')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    trigger_type = models.CharField(max_length=10, choices=TRIGGER_TYPES)
    
    # For Scheduled Triggers
    interval_type = models.CharField(max_length=20, choices=INTERVAL_TYPES, null=True, blank=True)
    interval_value = models.IntegerField(null=True, blank=True)
    fixed_time = models.TimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)
    next_run_at = models.DateTimeField(null=True, blank=True)
    
    # For API Triggers
    endpoint = models.CharField(max_length=500, null=True, blank=True)
    payload_schema = models.JSONField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_test = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.trigger_type == 'scheduled':
            self.calculate_next_run()
        super().save(*args, **kwargs)

    def calculate_next_run(self):
        now = timezone.now()
        if self.interval_type == 'minutes':
            self.next_run_at = now + timezone.timedelta(minutes=self.interval_value)
        elif self.interval_type == 'hours':
            self.next_run_at = now + timezone.timedelta(hours=self.interval_value)
        elif self.interval_type == 'fixed_time':
            next_run = timezone.make_aware(timezone.datetime.combine(
                timezone.now().date(),
                self.fixed_time
            ))
            if next_run <= now:
                next_run += timezone.timedelta(days=1)
            self.next_run_at = next_run