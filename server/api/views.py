from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests
from google_auth_oauthlib.flow import Flow
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import User, Order
from .serializers import UserSerializer, OrderSerializer
from .utils import send_order_confirmation

# Create your views here.

# Google OAuth2 flow initiator
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

def google_login(request):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    request.session['state'] = state
    return HttpResponseRedirect(authorization_url)

# Google login Callback handler
def google_callback(request):
    state = request.session.get('state')
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = settings.GOOGLE_REDIRECT_URI

    # Fetch the authorization response URL from the request
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    # ID token verification
    try:
        idinfo = id_token.verify_oauth2_token(
            credentials.id_token, requests.Request(), settings.GOOGLE_CLIENT_ID
        )

        # user info
        user_email = idinfo.get('email')
        user_name = idinfo.get('name')

        user, created = User.objects.get_or_create(email=user_email, defaults={
            'first_name': user_name.split()[0],
            'last_name': user_name.split()[1] if len(user_name.split()) > 1 else '',
            'is_google_user': True,
        })
        
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            'email': user.email,
            'name': user.name,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    except ValueError:
        return HttpResponseBadRequest('Invalid token')
    
def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.object.filter(user = self.request.user)

# Orders
class OrdersListCreateApiView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        request_data = self.request.data
        phone_number = request_data.get('phone_to_debit')
        order = serializer.save()
        order_details = f"Order ID: {order.id}, Item: {order.item}, Amount: {order.amount}"

        send_order_confirmation(phone_number, order_details)

        return Response({
            'message': 'Order created successfully and SMS sent.',
            'order_id': order.id
        })

class OrdersDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(customer = self.request.user)