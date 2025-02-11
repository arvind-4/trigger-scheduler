# backend/triggers/models.py
from django.db import models
from django.contrib.auth.models import User
from triggers.models import Trigger



class EventLog(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('archived', 'Archived')
    )
    
    trigger = models.ForeignKey(Trigger, on_delete=models.CASCADE)
    triggered_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    payload = models.JSONField(null=True, blank=True)
    response = models.JSONField(null=True, blank=True)
    is_test = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)