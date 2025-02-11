from eventlogs.models import EventLog
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required


@login_required
def event_log_list(request: HttpRequest):
    status = request.GET.get("status", "active")
    event_logs = EventLog.objects.filter(
        trigger_data__user_id=request.user.id, status=status
    ).select_related("trigger")
    return render(
        request,
        "eventlogs/event_logs.html",
        {"event_logs": event_logs, "status": status},
    )
