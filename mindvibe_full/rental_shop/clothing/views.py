from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Clothing, Favorite # เพิ่ม Favorite Model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required # สำหรับ @login_required
from django.conf import settings # สำหรับ settings.LOGIN_REDIRECT_URL

# หน้า Welcome
def welcome(request):
    return render(request, 'clothing/welcome.html')

# หน้าแสดงรายการเสื้อผ้า
def clothing_list(request):
    search_query = request.GET.get('search', '')
    color_filter = request.GET.get('color', '')
    clothes = Clothing.objects.all()
    if search_query:
        clothes = clothes.filter(name__icontains=search_query)
    if color_filter:
        clothes = clothes.filter(color__iexact=color_filter)
    return render(request, 'clothing/clothing_list.html', {'clothes': clothes, 'search_query': search_query, 'color': color_filter})

# หน้าแสดงรายละเอียดสินค้า
def clothing_detail(request, pk):
    clothing = get_object_or_404(Clothing, pk=pk)
    return render(request, 'clothing/clothing_detail.html', {'clothing': clothing})

# ฟังก์ชันค้นหาสินค้า (อันนี้ดูเหมือนจะซ้ำกับ logic ใน clothing_list นะครับ อาจจะพิจารณารวมกันหรือปรับปรุง)
def search_clothing(request):
    query = request.GET.get('q', '')
    clothes = Clothing.objects.filter(name__icontains=query)
    return render(request, 'clothing/clothing_list.html', {'clothes': clothes, 'query': query})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # หลังจากสมัครเสร็จ แนะนำให้ redirect ไปยังหน้า login โดยใช้ชื่อ URL
            # หรือถ้าต้องการให้ login ทันที ก็สามารถทำได้ แต่ปัจจุบันคือไปหน้า login
            return redirect('clothing:login') # สมมติว่า URL login ของคุณชื่อ 'login' ใน app_name 'clothing'
    else:
        form = UserCreationForm()
    # Template สำหรับ signup ควรอยู่ใน clothing/templates/clothing/signup.html ถ้าใช้ 'clothing/signup.html'
    # หรือ clothing/templates/signup.html ถ้าใช้ 'signup.html' และ Django หาเจอใน app clothing
    return render(request, 'clothing/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) # เพิ่ม request เข้า authenticate
            if user is not None:
                login(request, user)
                # จัดการ 'next' parameter สำหรับการ redirect
                next_url = request.POST.get('next') or request.GET.get('next') # ตรวจสอบ 'next' จาก POST และ GET
                if next_url:
                    # ตรวจสอบความปลอดภัยของ next_url (optional but recommended for production)
                    # from django.utils.http import url_has_allowed_host_and_scheme
                    # if url_has_allowed_host_and_scheme(url=next_url, allowed_hosts={request.get_host()}):
                    # return redirect(next_url)
                    return redirect(next_url) # สำหรับ development อาจจะใช้แบบนี้ไปก่อน
                else:
                    # ถ้าไม่มี 'next' ให้ redirect ไปยัง LOGIN_REDIRECT_URL
                    return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    else:
        form = AuthenticationForm()
    
    # ส่ง 'next' parameter ไปยัง template (ถ้ามีจากการ redirect ของ @login_required)
    next_url = request.GET.get('next')
    # Template สำหรับ login ควรอยู่ใน clothing/templates/clothing/login.html ถ้าใช้ 'clothing/login.html'
    return render(request, 'clothing/login.html', {'form': form, 'next': next_url})


@login_required # Decorator นี้จะตรวจสอบว่าผู้ใช้ล็อกอินหรือยัง
def favorites_list(request):
    # ดึงเฉพาะรายการ Favorite ของผู้ใช้ที่กำลังล็อกอินอยู่
    favorite_objects = Favorite.objects.filter(user=request.user).select_related('clothing')
    # ดึงเฉพาะตัว Clothing items จาก Favorite objects
    favorite_clothes = [fav.clothing for fav in favorite_objects]
    return render(request, 'clothing/favorites_list.html', {'favorite_clothes': favorite_clothes})