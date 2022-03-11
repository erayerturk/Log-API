from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import CustomUser


class LogTests(APITestCase):
    def setUp(self):
        self.username = "test"
        self.email = "test@test.com"
        self.password = "tester1234"
        self.user = CustomUser.objects.create_user(
            self.username, self.email, self.password
        )

    def test_log(self):
        url = reverse("token_obtain_pair")
        data = {"username": "test", "password": "tester1234"}
        response = self.client.post(url, data, format="json")
        access_token = "Bearer {0}".format(response.data.get("access"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        login_url = reverse("login")
        logout_url = reverse("logout")
        self.client.post(login_url, {}, HTTP_AUTHORIZATION=access_token)
        self.client.post(logout_url, {}, HTTP_AUTHORIZATION=access_token)

        ###
        log_url = reverse("log")
        response = self.client.get(
            log_url, {"q": "t", "is_active": True}, HTTP_AUTHORIZATION=access_token
        )
        # print(json.loads(response.content))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ###
        response = self.client.get(log_url, {"q": "x"}, HTTP_AUTHORIZATION=access_token)
        self.assertEqual(response.data, [])

        ###
        response = self.client.get(
            log_url, {"log_type": "loginx"}, HTTP_AUTHORIZATION=access_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        ###
        response = self.client.get(
            log_url,
            {"log_type": "login", "created": "2022-03-11,2022-03-11", "user_id": "1"},
            HTTP_AUTHORIZATION=access_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
