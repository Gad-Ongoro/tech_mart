import africastalking
from django.http import JsonResponse
from django.conf import settings

africastalking.initialize(settings.AFRICAS_TALKING_USERNAME, settings.AFRICAS_TALKING_API_KEY)

sms = africastalking.SMS

def send_order_confirmation(phone_number, order_details):
    message = f"Thank you for your order! Your order details are: {order_details}"

    try:
        response = sms.send(message, [phone_number])
        return JsonResponse({"success": True, "message": "SMS sent", "response": response}, status=200)

    except Exception as e:
        return JsonResponse({"success": False, "error": f"An unexpected error occurred: {str(e)}"}, status=500)