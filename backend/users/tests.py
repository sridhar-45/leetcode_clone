from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class AuthenticationAPITests(APITestCase):
    register_url = '/api/users/register/'
    login_url = '/api/users/login/'
    refresh_url = '/api/users/token/refresh/'
    logout_url = '/api/users/logout/'
    profile_url = '/api/users/profile/'

    def registration_payload(self, **overrides):
        payload = {
            'username': 'learner',
            'email': 'learner@example.com',
            'password': 'CodeRunner#4821',
            'password2': 'CodeRunner#4821',
            'first_name': 'Code',
            'last_name': 'Learner',
        }
        payload.update(overrides)
        return payload

    def register_user(self, **overrides):
        return self.client.post(
            self.register_url,
            self.registration_payload(**overrides),
            format='json',
        )

    def authenticate(self):
        response = self.register_user()
        access = response.data['tokens']['access']
        refresh = response.data['tokens']['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        return access, refresh

    def test_registration_creates_user_with_hashed_password_and_tokens(self):
        response = self.register_user()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

        user = User.objects.get(username='learner')
        self.assertNotEqual(user.password, 'CodeRunner#4821')
        self.assertTrue(check_password('CodeRunner#4821', user.password))

    def test_registration_rejects_duplicate_username(self):
        self.register_user()
        response = self.register_user(email='another@example.com')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        self.register_user()
        response = self.register_user(
            username='another-user',
            email='LEARNER@example.com',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_registration_rejects_password_mismatch(self):
        response = self.register_user(password2='DifferentPassword#1')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_registration_rejects_numeric_password(self):
        response = self.register_user(password='12345678', password2='12345678')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_returns_tokens_for_valid_credentials(self):
        self.register_user()
        response = self.client.post(
            self.login_url,
            {'username': 'learner', 'password': 'CodeRunner#4821'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_login_rejects_invalid_credentials(self):
        self.register_user()
        response = self.client.post(
            self.login_url,
            {'username': 'learner', 'password': 'wrong-password'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_requires_authentication(self):
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_token_authenticates_profile_request(self):
        self.authenticate()
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'learner')

    def test_refresh_token_returns_new_access_token(self):
        _, refresh = self.authenticate()
        self.client.credentials()
        response = self.client.post(
            self.refresh_url,
            {'refresh': refresh},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_blacklists_refresh_token(self):
        _, refresh = self.authenticate()
        response = self.client.post(
            self.logout_url,
            {'refresh': refresh},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials()
        refresh_response = self.client.post(
            self.refresh_url,
            {'refresh': refresh},
            format='json',
        )
        self.assertEqual(
            refresh_response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
