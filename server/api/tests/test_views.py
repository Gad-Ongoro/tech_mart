from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Order

User = get_user_model()

class UserViewTest(APITestCase):

    def test_user_creation(self):
        data = {
            'email': 'uniqueuser@gmail.com',
            'first_name': 'Unique',
            'last_name': 'User',
            'password': 'UniquePassword9911'
        }
        response = self.client.post(reverse('user-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'uniqueuser@gmail.com')

class OrderViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='uniqueuser@gmail.com',
            password='UniquePassword9911'
        )
        self.client.force_authenticate(user=self.user)

    def test_create_order(self):
        data = {
            'customer': self.user.id,
            'item': 'Test Product',
            'amount': 100,
            'phone_to_debit': '+254103004165'
        }
        response = self.client.post(reverse('order-list-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
