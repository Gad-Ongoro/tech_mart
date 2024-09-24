from django.test import TestCase
from django.contrib.auth import get_user_model
from api.models import Order

User = get_user_model()

class UserModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            first_name='Unique',
            last_name='User',
            email='uniqueuser@gmail.com',
            password='UniquePassword9911'
        )

    def test_create_user(self):
        """Test user is created successfully with an email"""
        self.assertEqual(self.user.email, 'uniqueuser@gmail.com')
        self.assertTrue(self.user.check_password('UniquePassword9911'))
        self.assertEqual(str(self.user), 'uniqueuser@gmail.com')

    def test_user_properties(self):
        """Test custom user properties"""
        self.assertEqual(self.user.name, 'Unique User')
        self.assertIsNotNone(self.user.code)

class OrderModelTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='uniqueuser@gmail.com',
            password='UniquePassword9911',
            first_name='Unique',
            last_name='User'
        )
        self.order = Order.objects.create(
            customer=self.user,
            item='Product X',
            amount=100,
            phone_to_debit='+254103004165'
        )
    
    def test_order_creation(self):
        """Test if the order is created successfully"""
        self.assertEqual(self.order.item, 'Product X')
        self.assertEqual(self.order.amount, 100)
        self.assertEqual(str(self.order), f'Order Product X by {self.user.name}')