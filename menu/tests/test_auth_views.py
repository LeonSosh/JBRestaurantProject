from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from menu.forms import RegistrationForm, UserLoginForm, UserUpdateForm


class TestAuthViews(TestCase):
    def setUp(self):
        """
        Sets up the necessary data for the test case.

        Parameters:
            self: The test case instance.

        Returns:
            None
        """
        self.client = Client()
        self.register_url = reverse("register")
        self.login_url = reverse("user_login")
        self.update_details_url = reverse("update_details")
        self.landing_page_url = reverse("landing_page")
        self.user_data = {
            "username": "testuser",
            "email": "test@email.com",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }
        self.user = User.objects.create_user(
            username=self.user_data["username"],
            email=self.user_data["email"],
            password=self.user_data["password1"],
        )
        self.register_user_data = {
            "username": "new_register_testuser",
            "email": "new_register_testuser@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Register",
            "last_name": "Testuser",
        }

    def assert_view_response(self, response, status_code, template_name, form_class):
        """
        Asserts that the given response object corresponds to the expected HTTP status code and
        the expected template used to render the response. The function also ensures that the response
        object is using the expected form class.

        :param response: A Django response object.
        :type response: django.http.response.HttpResponse

        :param status_code: The expected HTTP status code.
        :type status_code: int

        :param template_name: The expected name of the template used to render the response.
        :type template_name: str

        :param form_class: The expected form class used in the response object.
        :type form_class: django.forms.Form

        :return: None
        :rtype: None
        """
        self._extracted_from_test_user_login_view_post_2(
            response, status_code, template_name, form_class
        )

    def test_register_view_get(self):
        """
        Sends a GET request to the register view and checks if the response status code is 200.
        Also checks if the view used the 'register.html' template and rendered the RegistrationForm form.

        :param self: The instance of the test case class.
        :return: None
        """
        response = self.client.get(self.register_url)
        self.assert_view_response(response, 200, "register.html", RegistrationForm)

    def test_register_view_post(self):
        """
        Executes a test to register a new user. Sends a POST request to the register URL
        with the register user data and then checks the response status code. If the
        response status code is not 302, prints the form errors. Asserts that the response
        status code is 302 and that the response redirects to the landing page URL. Checks
        if the user exists in the database by filtering with the register user data's
        username field. Asserts that the user exists in the database.

        Args:
        - self: the object pointer.

        Returns:
        - None
        """
        response = self.client.post(self.register_url, data=self.register_user_data)
        if response.status_code != 302:
            print(response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        user_exists = User.objects.filter(username=self.register_user_data["username"]).exists()
        self.assertTrue(user_exists)

    def test_user_login_view_get(self):
        """
        Sends a GET request to the login URL of the user's login view and asserts that the response is valid.
        :param self: the instance of the test case being run.
        :return: None
        """
        response = self.client.get(self.login_url)
        self.assert_view_response(response, 200, "user_login.html", UserLoginForm)

    def test_user_login_view_post(self):
        """
        Sends a POST request to the login URL with the user's data as input parameters.
        Asserts that the response status code is 302 and that the user is redirected to the landing page URL.
        Sends another POST request to the login URL with the user's data but with an incorrect password.
        Calls _extracted_from_test_user_login_view_post_2 function with the response, 200, "user_login.html", and UserLoginForm as input parameters.
        Asserts that the "Invalid username or password." error message is displayed.
        """
        response = self.client.post(
            self.login_url,
            data={"username": self.user_data["username"], "password": self.user_data["password1"]},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        response = self.client.post(
            self.login_url,
            data={"username": self.user_data["username"], "password": "wrongpassword"},
        )
        self._extracted_from_test_user_login_view_post_2(
            response, 200, "user_login.html", UserLoginForm
        )
        error_message = any(
            "Invalid username or password." in message.message
            for message in response.context["messages"]
        )
        self.assertTrue(error_message)

    def _extracted_from_test_user_login_view_post_2(self, response, arg1, arg2, arg3):
        """
        Asserts that the response status code is equal to arg1 and that the
        response uses the template specified in arg2. Additionally, asserts that
        response.context["form"] is an instance of the type specified in arg3.

        :param response: the response object to be tested.
        :param arg1: the expected status code.
        :param arg2: the expected template name used to render the response.
        :param arg3: the expected type of response.context["form"].
        :return: None
        """
        self.assertEqual(response.status_code, arg1)
        self.assertTemplateUsed(response, arg2)
        self.assertIsInstance(response.context["form"], arg3)

    def post_user_login_view_data(self, password, expected_status_code=None):
        """
        Sends a POST request to the login URL with the username and password provided in the
        `self.user_data` dictionary along with the `password` parameter. If `expected_status_code`
        is not `None`, it asserts that the response status code is equal to `expected_status_code`.

        :param password: The password to be used in the login request.
        :type password: str

        :param expected_status_code: The expected response status code (optional).
        :type expected_status_code: int

        :return: The response object obtained after sending the POST request.
        :rtype: requests.Response
        """
        login_data = {
            "username": self.user_data["username"],
            "password": password,
        }
        response = self.client.post(self.login_url, data=login_data)
        if expected_status_code:
            self.assertEqual(response.status_code, expected_status_code)
        return response

    def test_update_details_view_get(self):
        """
        Test the functionality of the 'update details' view when accessed with GET request.

        :return: None
        """
        response = self.client.get(self.update_details_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.login_url}?next={self.update_details_url}")
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password1"]
        )
        response = self.client.get(self.update_details_url)
        self.assert_view_response(response, 200, "update_details.html", UserUpdateForm)

    def test_update_details_view_post(self):
        """
        This function tests the update_details view after a POST request. It logs in the user with the provided
        credentials, then sends a POST request to update the user's details. It asserts that the response status code is
        302, and that the page redirects to the landing page URL. It then retrieves the updated user details from the
        database and asserts that they match the updated details provided in the POST request.
        """
        self.client.login(
            username=self.user_data["username"], password=self.user_data["password1"]
        )
        update_data = {
            "first_name": "Updated",
            "last_name": "Testuser",
            "email": "updated_testuser@example.com",
        }
        response = self.client.post(self.update_details_url, data=update_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.landing_page_url)
        updated_user = User.objects.get(username=self.user_data["username"])
        self.assertEqual(updated_user.first_name, update_data["first_name"])
        self.assertEqual(updated_user.last_name, update_data["last_name"])
        self.assertEqual(updated_user.email, update_data["email"])
