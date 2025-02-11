import json
from datetime import time
from django.urls import reverse
from unittest.mock import patch
from triggers.models import Trigger
from django.test import TestCase, Client
from django.contrib.auth.models import User

class TriggerViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client = Client()
        self.trigger_data = {
            'name': 'Test Trigger',
            'trigger_type': 'webhook',
            'interval_type': 'minutes',
            'interval_value': 30,
            'fixed_time': time(12, 0),
            'endpoint': 'https://api.example.com/webhook',
            'payload_schema': json.dumps({'key': 'value'}),
            'is_recurring': True
        }
        self.trigger = Trigger.objects.create(
            user=self.user,
            **self.trigger_data
        )
        self.other_trigger = Trigger.objects.create(
            user=self.other_user,
            name='Other User Trigger',
            trigger_type='webhook',
            endpoint='https://api.example.com/webhook'
        )
        self.list_url = reverse('trigger_list')
        self.create_url = reverse('trigger_create')
        self.update_url = reverse('trigger_update', args=[self.trigger.pk])
        self.delete_url = reverse('trigger_delete', args=[self.trigger.pk])
        self.test_url = reverse('trigger_test', args=[self.trigger.pk])

    def test_login_required_all_views(self):
        urls = [
            self.list_url,
            self.create_url,
            self.update_url,
            self.delete_url,
            self.test_url
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            self.assertTrue("login" in response.url)

    def test_trigger_update_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('trigger_update', args=[self.other_trigger.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_trigger_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'triggers/trigger_confirm_delete.html')
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_url)
        self.assertFalse(Trigger.objects.filter(pk=self.trigger.pk).exists())

    def test_trigger_delete_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('trigger_delete', args=[self.other_trigger.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Trigger.objects.filter(pk=self.other_trigger.pk).exists())

    @patch('triggers.views.process_trigger.delay')
    def test_trigger_test_view(self, mock_process):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.test_url)
        self.assertEqual(response.status_code, 200)
        test_trigger = Trigger.objects.filter(
            user=self.user,
            name=f"Test - {self.trigger.name}",
            is_test=True
        ).first()
        self.assertIsNotNone(test_trigger)
        self.assertEqual(test_trigger.trigger_type, self.trigger.trigger_type)
        self.assertEqual(test_trigger.endpoint, self.trigger.endpoint)
        self.assertFalse(test_trigger.is_recurring)
        mock_process.assert_called_once_with(test_trigger.id)

    def test_trigger_test_other_user(self):
        self.client.login(username='testuser', password='testpass123')
        url = reverse('trigger_test', args=[self.other_trigger.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        Trigger.objects.all().delete()
        User.objects.all().delete()