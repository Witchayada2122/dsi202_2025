from django.db import models

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
