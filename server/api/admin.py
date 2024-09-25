from django.contrib import admin
from .models import User, Order

# Custom User Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_google_user', 'is_active', 'date_joined', 'updated_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_google_user', 'is_active')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('orders')

admin.site.register(User, UserAdmin)

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'item', 'amount', 'phone_to_debit', 'created_at', 'updated_at')
    search_fields = ('item', 'customer__email', 'phone_to_debit')
    list_filter = ('customer',)

admin.site.register(Order, OrderAdmin)
