import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import CustomUser, Company


class LogTests(APITestCase):
    def setUp(self):
        self.username = "test"
        self.email = "test@test.com"
        self.password = "tester1234"
        self.company = Company.objects.create(name="testCompany")
        self.user = CustomUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            company=self.company,
        )

        url = reverse("token_obtain_pair")
        data = {"username": "test", "password": "tester1234"}
        response = self.client.post(url, data, format="json")
        self.access_token = f"Bearer {response.data.get('access')}"

    def test_register(self):
        url = reverse("register")
        data = {
            "username": "admin",
            "password": "admin1234x",
            "password2": "admin1234x",
            "email": "admin@example.com",
            "company": "testcompany1",
        }
        response = self.client.post(url, data, format="json")
        response_sample = {"username": "admin", "email": "admin@example.com"}
        self.assertEqual(json.loads(response.content), response_sample)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse("login")
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logout(self):
        url = reverse("logout")
        response = self.client.post(url, {}, HTTP_AUTHORIZATION=self.access_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_log(self):
        log_url = reverse("log")
        response = self.client.get(
            log_url, {"q": "t", "is_active": True}, HTTP_AUTHORIZATION=self.access_token
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            log_url, {"q": "x"}, HTTP_AUTHORIZATION=self.access_token
        )
        self.assertEqual(response.data, [])

        response = self.client.get(
            log_url, {"log_type": "loginx"}, HTTP_AUTHORIZATION=self.access_token
        )
        response_sample = {
            "log_type": [
                "Select a valid choice. loginx is not one of the available choices."
            ]
        }
        self.assertEqual(json.loads(response.content), response_sample)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            log_url,
            {"log_type": "login", "created": "2022-03-11,2022-03-11", "user_id": "1"},
            HTTP_AUTHORIZATION=self.access_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
