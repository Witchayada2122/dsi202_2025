from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Clothing, Favorite  # เพิ่ม Favorite Model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required  # สำหรับ @login_required
from django.conf import settings  # สำหรับ settings.LOGIN_REDIRECT_URL

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

# หน้า Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clothing:login')  # ไปที่หน้า login
    else:
        form = UserCreationForm()
    return render(request, 'clothing/signup.html', {'form': form})

# หน้า Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    else:
        form = AuthenticationForm()
    next_url = request.GET.get('next')
    return render(request, 'clothing/login.html', {'form': form, 'next': next_url})

# หน้า Favorites (ต้องล็อกอิน)
@login_required
def favorites_list(request):
    # ดึงรายการ Favorite ของผู้ใช้ที่ล็อกอิน
    favorite_objects = Favorite.objects.filter(user=request.user).select_related('clothing')
    favorite_clothes = [fav.clothing for fav in favorite_objects]
    return render(request, 'clothing/favorites_list.html', {'favorite_clothes': favorite_clothes})

# ฟังก์ชันเพิ่มสินค้าลงในรายการโปรด
@login_required
def add_to_favorites(request, pk):
    clothing_item = get_object_or_404(Clothing, pk=pk)
    
    # เช็คว่าผู้ใช้ได้เพิ่มสินค้าลงในรายการโปรดหรือยัง
    if not Favorite.objects.filter(user=request.user, clothing=clothing_item).exists():
        # เพิ่มสินค้าไปในรายการโปรด
        Favorite.objects.create(user=request.user, clothing=clothing_item)
    
    return redirect('clothing:favorites_list')  # ไปหน้า favorites_list เมื่อเพิ่มเสร็จแล้ว

# ฟังก์ชันสำหรับหน้าตะกร้าสินค้า
def cart(request):
    return render(request, 'clothing/cart.html')

# ฟังก์ชันสำหรับหน้าสถานะการจัดส่ง
def status(request):
    return render(request, 'clothing/status.html')

# ฟังก์ชันสำหรับหน้าข้อมูลโปรไฟล์
def profile(request):
    return render(request, 'clothing/profile.html')
