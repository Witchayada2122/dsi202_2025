from django.contrib import admin
from .models import Clothing, ClothingType, Payment, OrderStatus  # เพิ่ม OrderStatus

# ----------------- Clothing Admin -----------------
class ClothingAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price_per_day_1', 'price_per_day_3',
        'price_per_day_5', 'price_per_day_7',
        'available', 'color', 'material', 'fit',
        'design', 'clothing_type'
    )
    list_filter = (
        'available', 'color', 'material', 'fit', 'design', 'clothing_type'
    )
    search_fields = (
        'name', 'product_details', 'color', 'material', 'fit',
        'design', 'versatility', 'sizes_available', 'care_instructions', 'perfect_for'
    )
    fieldsets = (
        (None, {
            'fields': (
                'name', 'product_details', 'price_per_day_1', 'price_per_day_3',
                'price_per_day_5', 'price_per_day_7', 'image', 'color', 'available',
                'material', 'fit', 'design', 'versatility', 'sizes_available',
                'care_instructions', 'perfect_for', 'clothing_type'
            )
        }),
    )

# ----------------- Inline Order Status -----------------
class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 1
    readonly_fields = ('updated_at',)

# ----------------- Payment Admin -----------------
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone_number', 'total_price', 'payment_date')
    search_fields = ('user__username', 'full_name', 'phone_number')
    readonly_fields = ('payment_date',)
    inlines = [OrderStatusInline]  # แสดง OrderStatus แบบ inline

# ----------------- Register -----------------
admin.site.register(Payment, PaymentAdmin)
admin.site.register(OrderStatus)  # ลงทะเบียน OrderStatus แยก
admin.site.register(Clothing, ClothingAdmin)
admin.site.register(ClothingType)
