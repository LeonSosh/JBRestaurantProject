from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from menu.models import Category, Dish, Cart, Item, Delivery
from menu.views.delivery_views import ManageDeliveriesView, MarkAsDeliveredView, ViewOrderHistoryView
from django.core.files.uploadedfile import SimpleUploadedFile


class DeliveryViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        image_file = SimpleUploadedFile(
            "test_image.jpg", b"file_content", content_type="image/jpeg")
        self.category = Category.objects.create(name="Test Category", image=image_file)
        self.dish = Dish.objects.create(
            name="Test Dish",
            price=9.99,
            description="Test dish description",
            image=image_file,
            is_gluten_free=False,
            is_vegetarian=False,
            category=self.category
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user.save()
        self.cart = Cart.objects.create(user=self.user, is_active=True)
        self.cart.save()
        self.item = Item.objects.create(
            dish=self.dish, cart=self.cart, amount=1, dish_name=self.dish.name, dish_price=self.dish.price)
        self.item.save()
        self.delivery = Delivery.objects.create(address="Test Address", cart=self.cart)
        self.delivery.save()
        self.manager_group = Group.objects.create(name='manager')
        self.manager_user = User.objects.create_user(
            username='manager', password='managerpassword')
        self.manager_group.user_set.add(self.manager_user)

    def test_manage_deliveries_view(self):
        request = self.factory.get('/manage_deliveries/')
        request.user = self.manager_user
        response = ManageDeliveriesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['deliveries']), 1)

    def test_mark_as_delivered_view(self):
        request = self.factory.post('/mark_as_delivered/')
        request.user = self.manager_user
        response = MarkAsDeliveredView.as_view()(request, delivery_id=self.delivery.id)
        self.assertEqual(response.status_code, 302)
        self.delivery.refresh_from_db()
        self.assertTrue(self.delivery.is_delivered)

    def test_view_order_history_view(self):
        request = self.factory.get('/order_history/')
        request.user = self.user
        response = ViewOrderHistoryView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context_data['orders']), 1)
