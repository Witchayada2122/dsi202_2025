from django import forms
from django.contrib.auth.models import User

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=50,  # กำหนดจำนวนตัวอักษรสูงสุดที่ 50
        min_length=3,   # กำหนดจำนวนตัวอักษรขั้นต่ำที่ 3
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'กรอกชื่อผู้ใช้'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'กรอกอีเมลของคุณ'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'กรอกรหัสผ่าน'}),
        min_length=8,
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'ยืนยันรหัสผ่าน'}),
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # เพิ่ม email เข้าไปใน fields

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # ตรวจสอบว่ารหัสผ่านตรงกันหรือไม่
        if password1 != password2:
            raise forms.ValidationError("รหัสผ่านไม่ตรงกัน")

        # ตรวจสอบว่าอีเมลซ้ำกับที่มีในฐานข้อมูลหรือไม่
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("อีเมลนี้ถูกใช้งานแล้ว")

        return cleaned_data
