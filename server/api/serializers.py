from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'code', 'first_name', 'last_name', 'name', 'email', 'password', 'is_google_user', 'is_active', 'date_joined', 'updated_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'code': {'read_only': True},
            'is_google_user': {'read_only': True},
            'password':  {'write_only': True},
            'is_active': {'read_only': True},
            'date_joined': {'read_only': True},
            'updated_at': {'read_only': True}
        }

    def create(self, validated_data):
        if not validated_data.get('is_google_user', False):
            validated_data['password'] = make_password(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer', 'item', 'amount', 'phone_to_debit', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'id':  {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
