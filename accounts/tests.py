from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.home_url = reverse("home")
        self.test_user = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        self.existing_user = User.objects.create_user(
            username="existinguser", password="existing123"
        )

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_register_POST_success(self):
        response = self.client.post(self.register_url, self.test_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertTrue(
            User.objects.filter(username=self.test_user["username"]).exists()
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Account created successfully!")

    def test_register_POST_invalid_data(self):
        invalid_user = {
            "username": "testuser",
            "password1": "test123",
            "password2": "different123",
        }
        response = self.client.post(self.register_url, invalid_user)
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Error in registration. Please try again.")
        self.assertFalse(
            User.objects.filter(username=invalid_user["username"]).exists()
        )

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_login_POST_success(self):
        response = self.client.post(
            self.login_url, {"username": "existinguser", "password": "existing123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_POST_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"username": "existinguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Invalid credentials. Please try again.")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_logout_view(self):
        self.client.login(username="existinguser", password="existing123")
        self.assertTrue("_auth_user_id" in self.client.session)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)
        self.assertFalse("_auth_user_id" in self.client.session)
