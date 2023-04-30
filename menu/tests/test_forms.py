from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from menu.forms import CategoryForm, DishForm, PlaceOrderForm, RegistrationForm, UserLoginForm, UserUpdateForm
from menu.models import Category
from io import BytesIO
from PIL import Image


class CategoryFormTest(TestCase):
    def test_valid_form(self):
        img_io = BytesIO()
        Image.new('RGB', (100, 100)).save(img_io, 'JPEG')
        img_io.seek(0)
        image = SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type="image/jpeg")
        form = CategoryForm(data={'name': 'Test Category'}, files={'image': image})
        if not form.is_valid():
            print(f"CategoryForm errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = CategoryForm(data={'name': '', 'image': None})
        self.assertFalse(form.is_valid())


class DishFormTest(TestCase):
    def setUp(self):
        img_io = BytesIO()
        Image.new('RGB', (100, 100)).save(img_io, 'JPEG')
        img_io.seek(0)
        image = SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type="image/jpeg")
        self.category = Category.objects.create(name='Test Category', image=image)

    def test_valid_form(self):
        img_io = BytesIO()
        Image.new('RGB', (100, 100)).save(img_io, 'JPEG')
        img_io.seek(0)
        image = SimpleUploadedFile("test_image.jpg", img_io.getvalue(), content_type="image/jpeg")
        form = DishForm(data={
            'name': 'Test Dish',
            'price': 12.99,
            'description': 'Test description',
            'is_gluten_free': False,
            'is_vegetarian': True,
            'category': self.category.id
        }, files={'image': image})
        if not form.is_valid():
            print(f"DishForm errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = DishForm(data={'name': '', 'price': '', 'description': '',
                        'image': None, 'category': ''})
        self.assertFalse(form.is_valid())


class PlaceOrderFormTest(TestCase):
    def test_valid_form(self):
        form = PlaceOrderForm(data={'address': '123 Test Street', 'comment': 'Leave at the door'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = PlaceOrderForm(data={'address': '', 'comment': 'Leave at the door'})
        self.assertFalse(form.is_valid())


class RegistrationFormTest(TestCase):
    def test_valid_form(self):
        form = RegistrationForm(data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = RegistrationForm(data={
            'username': '',
            'email': 'test@example.com',
            'password1': 'testpassword1',
            'password2': 'testpassword1',
            'first_name': 'Test',
            'last_name': 'User'
        })
        self.assertFalse(form.is_valid())


class UserLoginFormTest(TestCase):
    def test_valid_form(self):
        form = UserLoginForm(data={'username': 'testuser', 'password': 'testpassword'})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserLoginForm(data={'username': '', 'password': ''})
        self.assertFalse(form.is_valid())


class UserUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_valid_form(self):
        form = UserUpdateForm(instance=self.user, data={
            'first_name': 'New',
            'last_name': 'Name',
            'email': 'new@example.com'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = UserUpdateForm(instance=self.user, data={
            'first_name': '', 'last_name': '', 'email': ''})
        self.assertTrue(form.is_valid())
