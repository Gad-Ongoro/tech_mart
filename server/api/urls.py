from django.urls import path
from .views import (
    UserCreateApiView, 
    UserListApiView, 
    UserDetailApiView, 
    OrdersListCreateApiView, 
    OrdersDetailApiView,
    google_login,
    google_callback
)

urlpatterns = [
    # User URLs
    path('users/', UserListApiView.as_view(), name='user-list'),
    path('users/register/', UserCreateApiView.as_view(), name='user-create'), # for normal signups
    path('users/<uuid:pk>/', UserDetailApiView.as_view(), name='user-detail'),

    # Google OAuth2 URLs
    path('google/login/', google_login, name='google-login'),
    path('oauth2callback/', google_callback, name='google-callback'),

    # Order URLs
    path('orders/', OrdersListCreateApiView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrdersDetailApiView.as_view(), name='order-detail'),
]
