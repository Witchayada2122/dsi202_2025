from django.db import models
from django.contrib.auth.models import User # <--- เพิ่มบรรทัดนี้!

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

    # เพิ่มฟิลด์ราคาเช่า
    price_per_day_1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_5 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day_7 = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    clothing = models.ForeignKey(Clothing, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clothing') # ป้องกันการกดโปรดซ้ำสำหรับสินค้าชิ้นเดียวกันโดยผู้ใช้คนเดียว
        ordering = ['-added_at'] # เรียงจากรายการที่เพิ่มล่าสุดก่อน

    def __str__(self):
        return f"{self.user.username} favorites {self.clothing.name}"