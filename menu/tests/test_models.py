import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from menu.models import Cart, Category, Delivery, Dish, Item


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Test Category", image=None)
        self.assertEqual(category.name, "Test Category")
        self.assertIsNotNone(category.image)


class DishModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category", image=None)

    def test_create_dish(self):
        dish = Dish.objects.create(
            name="Test Dish",
            price=Decimal("10.99"),
            description="Test description",
            image=None,
            is_gluten_free=False,
            is_vegetarian=True,
            category=self.category
        )
        self.assertEqual(dish.name, "Test Dish")
        self.assertEqual(dish.price, Decimal("10.99"))
        self.assertEqual(dish.description, "Test description")
        self.assertIsNotNone(dish.image)
        self.assertFalse(dish.is_gluten_free)
        self.assertTrue(dish.is_vegetarian)
        self.assertEqual(dish.category, self.category)


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )

    def test_create_cart(self):
        cart = Cart.objects.create(user=self.user, is_active=True)
        self.assertEqual(cart.user, self.user)
        self.assertTrue(cart.is_active)


class ItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.category = Category.objects.create(name="Test Category", image=None)
        self.dish = Dish.objects.create(
            name="Test Dish",
            price=Decimal("10.99"),
            description="Test description",
            image=None,
            is_gluten_free=False,
            is_vegetarian=True,
            category=self.category
        )

    def test_create_item(self):
        item = Item.objects.create(
            dish=self.dish,
            cart=self.cart,
            amount=2,
            dish_name=self.dish.name,
            dish_price=self.dish.price
        )
        self.assertEqual(item.dish, self.dish)
        self.assertEqual(item.cart, self.cart)
        self.assertEqual(item.amount, 2)
        self.assertEqual(item.dish_name, "Test Dish")
        self.assertEqual(item.dish_price, Decimal("10.99"))


class DeliveryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.cart = Cart.objects.create(user=self.user, is_active=True)

    def tearDown(self):
        self.user.delete()

    def test_create_delivery(self):
        delivery = Delivery.objects.create(
            is_delivered=False,
            address='123 Test St',
            comment='Leave at the front door',
            cart=self.cart,
            delivery_time=timezone.now() + datetime.timedelta(hours=2),
            delivery_fee=5.00
        )
        self.assertEqual(delivery.is_delivered, False)
        self.assertEqual(delivery.address, '123 Test St')
        self.assertEqual(delivery.comment, 'Leave at the front door')
        self.assertEqual(delivery.cart, self.cart)
        self.assertEqual(delivery.delivery_fee, 5.00)
