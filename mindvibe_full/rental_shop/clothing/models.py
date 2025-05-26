import uuid
from django.db import models
from django.contrib.auth.models import User


# สร้างคลาส ClothingType ที่เก็บประเภทเสื้อผ้า
class ClothingType(models.Model):
    name = models.CharField(max_length=100)  # ชื่อประเภทเสื้อผ้า (เช่น เสื้อครอป, เสื้อ, เดรส)
    
    def __str__(self):
        return self.name

# โมเดลสำหรับ Clothing
class Clothing(models.Model):
    name = models.CharField(max_length=100)
    product_details = models.TextField()

    image = models.ImageField(upload_to='clothing_images/')
    color = models.CharField(max_length=20, default="N/A")
    available = models.BooleanField(default=True)

    material = models.CharField(max_length=200, default="N/A")
    fit = models.CharField(max_length=200, default="N/A")
    design = models.CharField(max_length=200, default="N/A")
    versatility = models.CharField(max_length=200, default="N/A")
    sizes_available = models.CharField(max_length=200, default="N/A")
    care_instructions = models.TextField(default="N/A")
    perfect_for = models.TextField(default="N/A")

    # เพิ่มฟิลด์ประเภทเสื้อผ้า
    clothing_type = models.ForeignKey(ClothingType, on_delete=models.SET_NULL, null=True, blank=True)

    # เพิ่มฟิลด์ราคาเช่า
    price_per_day_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_7 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

# ส่วนของ Favorite และ Payment สามารถคงเดิม
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clothing')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user.username} favorites {self.clothing.name}"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default="-")
    address = models.TextField(default="-")
    phone_number = models.CharField(max_length=20, default="-")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    proof = models.ImageField(upload_to='payment_proofs/')
    payment_date = models.DateTimeField(auto_now_add=True)
    return_proof = models.ImageField(upload_to='return_proofs/', blank=True, null=True)
    return_item_code = models.CharField(max_length=100, blank=True, null=True)
    payment_ref = models.UUIDField(default=uuid.uuid4, unique=True)
    qr_base64 = models.TextField(blank=True, null=True)

    def get_qr_base64(self):
        if not self.qr_base64:
            from .views import generate_promptpay_qr
            self.qr_base64 = generate_promptpay_qr(self)
            self.save()
        return self.qr_base64

    def __str__(self):
        return f"Payment for {self.user.username} - {self.total_price} THB"

class OrderStatus(models.Model):
    STATUS_CHOICES = [
        ('paid', 'ชำระเงินเรียบร้อยแล้ว'),
        ('packing', 'จัดเตรียมสินค้าแล้ว'),
        ('shipping', 'ดำเนินการจัดส่งแล้ว'),
        ('shipped', 'จัดส่งสำเร็จแล้ว'),
        ('returned', 'ได้รับคืนสินค้าเรียบร้อยแล้ว'),
    ]
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment} - {self.get_status_display()}"


