from django.test import TestCase
from unittest.mock import patch
from api.utils import send_order_confirmation

class SendSMSUtilsTest(TestCase):

    @patch('api.utils.sms.send')
    def test_send_order_confirmation(self, mock_send):
        mock_send.return_value = 'SMS Sent'

        response = send_order_confirmation('+254103004165', 'Order details')
        mock_send.assert_called_once_with('Thank you for your order! Your order details are: Order details', ['+254103004165'])
        self.assertEqual(mock_send.return_value, 'SMS Sent')
