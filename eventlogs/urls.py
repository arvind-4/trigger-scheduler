from django.urls import path
from eventlogs.views import event_log_list

urlpatterns = [
    path("", event_log_list, name="event_log_list"),
]
