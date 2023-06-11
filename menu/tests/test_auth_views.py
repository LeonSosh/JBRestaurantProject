from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from menu.forms import RegistrationForm, UserLoginForm, UserUpdateForm


class TestAuthViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('user_login')
        self.update_details_url = reverse('update_details')
        self.landing_page_url = reverse('landing_page')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@email.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            email=self.user_data['email'],
            password=self.user_data['password1']
        )
        self.register_user_data = {
            'username': 'new_register_testuser',
            'email': 'new_register_testuser@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Register',
            'last_name': 'Testuser',
        }

    def assert_view_response(self, response, status_code, template_name, form_class):
        self._extracted_from_test_user_login_view_post_2(
            response, status_code, template_name, form_class
        )

    def test_register_view_get(self):
        response = self.client.get(self.register_url)
        self.assert_view_response(response, 200, 'register.html', RegistrationForm)

    def test_register_view_post(self):
        response = self.client.post(self.register_url, data=self.register_user_data)
        if response.status_code != 302:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        user_exists = User.objects.filter(username=self.register_user_data['username']).exists()
        self.assertTrue(user_exists)

    def test_user_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assert_view_response(response, 200, 'user_login.html', UserLoginForm)

    def test_user_login_view_post(self):
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': self.user_data['password1']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        response = self.client.post(self.login_url, data={
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        })
        self._extracted_from_test_user_login_view_post_2(
            response, 200, 'user_login.html', UserLoginForm
        )
        error_message = any(
            'Invalid username or password.' in message.message
            for message in response.context['messages']
        )
        self.assertTrue(error_message)

    # TODO Rename this here and in `assert_view_response` and `test_user_login_view_post`
    def _extracted_from_test_user_login_view_post_2(self, response, arg1, arg2, arg3):
        self.assertEqual(response.status_code, arg1)
        self.assertTemplateUsed(response, arg2)
        self.assertIsInstance(response.context['form'], arg3)

    def post_user_login_view_data(self, password, expected_status_code=None):
        login_data = {
            'username': self.user_data['username'],
            'password': password,
        }
        response = self.client.post(self.login_url, data=login_data)
        if expected_status_code:
            self.assertEqual(response.status_code, expected_status_code)
        return response

    def test_update_details_view_get(self):
        response = self.client.get(self.update_details_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{self.login_url}?next={self.update_details_url}')
        self.client.login(username=self.user_data['username'],
                          password=self.user_data['password1'])
        response = self.client.get(self.update_details_url)
        self.assert_view_response(response, 200, 'update_details.html', UserUpdateForm)

    def test_update_details_view_post(self):
        self.client.login(username=self.user_data['username'],
                          password=self.user_data['password1'])
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Testuser',
            'email': 'updated_testuser@example.com',
        }
        response = self.client.post(self.update_details_url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        updated_user = User.objects.get(username=self.user_data['username'])
        self.assertEqual(updated_user.first_name, update_data['first_name'])
        self.assertEqual(updated_user.last_name, update_data['last_name'])
        self.assertEqual(updated_user.email, update_data['email'])
