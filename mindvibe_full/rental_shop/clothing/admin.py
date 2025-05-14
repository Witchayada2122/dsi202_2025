from django.contrib import admin
from .models import Clothing, ClothingType

class ClothingAdmin(admin.ModelAdmin):
    # กำหนดฟิลด์ที่จะแสดงในหน้า Admin
    list_display = ('name', 'price_per_day_1', 'price_per_day_3', 'price_per_day_5', 'price_per_day_7', 'available', 'color', 'material', 'fit', 'design', 'clothing_type')  # เพิ่ม 'clothing_type'
    list_filter = ('available', 'color', 'material', 'fit', 'design', 'clothing_type')  # เพิ่มตัวกรองตามประเภทเสื้อผ้า
    search_fields = ('name', 'product_details', 'color', 'material', 'fit', 'design', 'versatility', 'sizes_available', 'care_instructions', 'perfect_for')  # ค้นหาจากฟิลด์ต่างๆ

    # สามารถเพิ่มฟิลด์ที่ต้องการให้แก้ไขในหน้า Admin ได้
    fieldsets = (
        (None, {
            'fields': ('name', 'product_details', 'price_per_day_1', 'price_per_day_3', 'price_per_day_5', 'price_per_day_7', 'image', 'color', 'available', 'material', 'fit', 'design', 'versatility', 'sizes_available', 'care_instructions', 'perfect_for', 'clothing_type')  # เพิ่ม 'clothing_type'
        }),
    )

# ลงทะเบียนโมเดล Clothing และ ClothingType กับหน้า Admin
admin.site.register(Clothing, ClothingAdmin)
admin.site.register(ClothingType)  # ลงทะเบียน ClothingType
