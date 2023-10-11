from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

class RegisterTestCase(APITestCase):
    """
    Test case for user registration.

    This test case includes tests for user registration functionality.

    Test methods:
    - test_register: Tests user registration with valid data.
    """
    def test_register(self):
        """
        Test user registration with valid data.

        This test sends a POST request to the registration endpoint with valid data
        and expects a successful response (HTTP 201 Created).
        """
        data = {
            "username": "Toqa",
            "email": "toqa@gmail.com",
            "password": "Toqawasfi12",
            "password2": "Toqawasfi12"
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginLogoutTestCase(APITestCase):
    """

    This test case includes tests for user login and logout functionality.

    Test methods:
    - test_login: Tests user login with valid credentials.
    - test_logout: Tests user logout.
    - test_send_email: Tests sending a password reset email.
    - test_password_reset: Tests resetting the user's password.
    """
    def setUp(self):
        self.user = User.objects.create_user(username="Toqa", password="Toqawasfi12", email="toqa@gmail.com")

    def test_login(self):
        """
        Test user login with valid credentials.

        This test sends a POST request to the login endpoint with valid credentials
        and expects a successful response (HTTP 200 OK).
        """
        data = {
            "username": "Toqa",
            "password": "Toqawasfi12"
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        """
        Test user logout.

        This test logs in a user, sends a POST request to the logout endpoint,
        and expects a successful response (HTTP 200 OK) indicating successful logout.
        """
        self.token = Token.objects.get(user__username="Toqa")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_send_email(self):
        """
        Test sending a password reset email.

        This test sends a POST request to the send-email endpoint with valid data
        and expects a successful response (HTTP 200 OK).
        """
        data = {
            "username": "Toqa",
            "email": "toqa@gmail.com"
        }
        response = self.client.post(reverse('send-email'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset(self):
        """
        Test resetting the user's password.

        This test sends a POST request to the password_reset endpoint with valid data
        and expects a successful response (HTTP 200 OK).
        """
        data = {
            "username": "Toqa",
            "email": "toqa@gmail.com",
            "new_password": "Banyyassen12"
        }
        response = self.client.post(reverse('password_reset'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
