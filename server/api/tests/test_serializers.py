from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import Order
from api.serializers import UserSerializer, OrderSerializer

User = get_user_model()

class UserSerializerTest(TestCase):

    def setUp(self):
        self.user_data = {
            'first_name' : 'Unique',
            'last_name' : 'User',
            'email' : 'uniqueuser@gmail.com',
            'password' : 'UniquePassword9911'
        }

    def test_user_serializer(self):
        serializer = UserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'uniqueuser@gmail.com')
        self.assertTrue(user.check_password('UniquePassword9911'))

class OrderSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='uniqueuser@gmail.com',
            password='UniquePassword9911',
            first_name='Unique',
            last_name='User'
        )
        self.order_data = {
            'customer': self.user.id,
            'item': 'Product X',
            'amount': 100,
            'phone_to_debit': '+254103004165'
        }

    def test_order_serializer(self):
        serializer = OrderSerializer(data=self.order_data)
        self.assertTrue(serializer.is_valid())
        order = serializer.save()
        self.assertEqual(order.item, 'Product X')
        self.assertEqual(order.amount, 100)
