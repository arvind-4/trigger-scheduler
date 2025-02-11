import json
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from eventlogs.models import EventLog, Trigger


class EventLogListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client = Client()
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.trigger1 = Trigger.objects.create(name="Test Trigger 1", user=self.user)
        self.trigger2 = Trigger.objects.create(name="Test Trigger 2", user=self.user)
        self.active_log = EventLog.objects.create(
            trigger=self.trigger1,
            trigger_data=json.dumps({"user_id": self.user.id}),
            status="active",
        )
        self.completed_log = EventLog.objects.create(
            trigger=self.trigger2,
            trigger_data=json.dumps({"user_id": self.user.id}),
            status="completed",
        )
        self.other_user_trigger = Trigger.objects.create(
            name="Other User Trigger", user=self.other_user
        )
        self.other_user_log = EventLog.objects.create(
            trigger=self.other_user_trigger,
            trigger_data=json.dumps({"user_id": self.other_user.id}),
            status="active",
        )
        self.url = reverse("event_log_list")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue("login" in response.url)

    def test_event_log_list_active(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "eventlogs/event_logs.html")
        self.assertEqual(response.context["status"], "active")
        event_logs = response.context["event_logs"]
        self.assertEqual(len(event_logs), 1)
        self.assertEqual(event_logs[0], self.active_log)
        self.assertNotIn(self.other_user_log, event_logs)

    def tearDown(self):
        EventLog.objects.all().delete()
        Trigger.objects.all().delete()
        User.objects.all().delete()
