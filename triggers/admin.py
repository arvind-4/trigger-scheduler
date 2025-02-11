from django.contrib import admin

# Register your models here.

from triggers.models import Trigger

admin.site.register(Trigger)