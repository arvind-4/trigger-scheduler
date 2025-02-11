import logging
import requests
from django.apps import apps
from celery import shared_task
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def process_trigger(trigger_id):
    Trigger = apps.get_model("triggers", "Trigger")
    EventLog = apps.get_model("eventlogs", "EventLog")
    try:
        logger.info(f"Trigger {trigger_id} started")
        trigger = Trigger.objects.get(id=trigger_id)
        event_log = EventLog.objects.create(trigger=trigger, is_test=trigger.is_test)

        if trigger.trigger_type == "scheduled":
            if trigger.is_recurring and not trigger.is_test:
                trigger.calculate_next_run()
                trigger.save()
            else:
                trigger.is_active = False
                trigger.save()

        elif trigger.trigger_type == "api":
            try:
                response = requests.post(
                    trigger.endpoint,
                    json=trigger.payload_schema,
                    headers={"Content-Type": "application/json"},
                )

                event_log.payload = trigger.payload_schema
                event_log.response = {
                    "status_code": response.status_code,
                    "content": response.text,
                }
                event_log.save()

            except Exception as e:
                event_log.error = str(e)
                event_log.save()
        logger.info(f"Trigger {trigger_id} completed")
        return True

    except Exception as e:
        logger.error(f"Error processing trigger {trigger_id}: {str(e)}")
        return False


@shared_task
def run_scheduled_triggers():
    Trigger = apps.get_model("triggers", "Trigger")

    now = timezone.now()
    due_triggers = Trigger.objects.filter(is_active=True, next_run_at__lte=now)

    for trigger in due_triggers:
        logger.info(f"Scheduling trigger {trigger.id}")
        process_trigger.delay(trigger.id)
        logger.info(f"Scheduled trigger {trigger.id}")


@shared_task
def manage_event_logs():
    EventLog = apps.get_model("eventlogs", "EventLog")
    two_hours_ago = timezone.now() - timedelta(hours=2)
    EventLog.objects.filter(status="active", triggered_at__lt=two_hours_ago).update(
        status="archived"
    )
    forty_eight_hours_ago = timezone.now() - timedelta(hours=48)
    EventLog.objects.filter(triggered_at__lt=forty_eight_hours_ago).delete()
