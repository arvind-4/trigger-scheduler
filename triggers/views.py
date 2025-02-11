from triggers.models import Trigger
from triggers.forms import TriggerForm
from triggers.tasks import process_trigger
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def trigger_list(request: HttpRequest):
    triggers = Trigger.objects.filter(user=request.user, is_test=False)
    return render(request, "triggers/trigger_list.html", {"triggers": triggers})

@login_required
def trigger_create(request: HttpRequest):
    form = TriggerForm(request.POST or None)
    if form.is_valid():
        trigger = form.save(commit=False)
        trigger.user = request.user
        trigger.save()
        process_trigger.delay(trigger.id)
        return redirect("trigger_list")
    return render(request, "triggers/trigger_form.html", {"form": form})

@login_required
def trigger_update(request: HttpRequest, pk: int):
    trigger = get_object_or_404(Trigger, pk=pk, user=request.user)
    if request.method == "POST":
        form = TriggerForm(request.POST, instance=trigger)
        if form.is_valid():
            form.save()
            process_trigger.delay(trigger.id)
            return redirect("trigger_list")
    else:
        form = TriggerForm(instance=trigger)
    return render(request, "triggers/trigger_form.html", {"form": form})

@login_required
def trigger_delete(request: HttpRequest, pk: int):
    trigger = get_object_or_404(Trigger, pk=pk, user=request.user)
    if request.method == "POST":
        trigger.delete()
        return redirect("trigger_list")
    return render(request, "triggers/trigger_confirm_delete.html", {"trigger": trigger})

@login_required
def trigger_test(request: HttpRequest, pk: int):
    original_trigger = get_object_or_404(Trigger, pk=pk, user=request.user)

    test_trigger = Trigger.objects.create(
        user=request.user,
        name=f"Test - {original_trigger.name}",
        trigger_type=original_trigger.trigger_type,
        interval_type=original_trigger.interval_type,
        interval_value=original_trigger.interval_value,
        fixed_time=original_trigger.fixed_time,
        endpoint=original_trigger.endpoint,
        payload_schema=original_trigger.payload_schema,
        is_test=True,
        is_recurring=False,
    )
    process_trigger.delay(test_trigger.id)
    return HttpResponse(f"Test trigger created and scheduled with ID {test_trigger.id}")
