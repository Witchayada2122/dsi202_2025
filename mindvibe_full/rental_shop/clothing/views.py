from django.shortcuts import render, get_object_or_404, redirect
from .models import Clothing, Favorite
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings

# ฟังก์ชันสำหรับดึงข้อมูลสินค้าจากตะกร้า
def get_cart_items(request):
    cart = request.session.get('cart', [])
    cart_items = []
    
    for item in cart:
        try:
            product = get_object_or_404(Clothing, pk=item['product_id'])
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'total': product.price * item['quantity']
            })
        except (KeyError, Clothing.DoesNotExist):
            # ข้ามรายการที่มีปัญหา (เช่น product_id ไม่ถูกต้อง)
            continue
    return cart_items

# ฟังก์ชันสำหรับหน้าตะกร้าสินค้า
def cart(request):
    cart_items = get_cart_items(request)
    total_price = 0

    for item in cart_items:
        total_price += item['total']

    formatted_total_price = f"฿ {total_price:,.2f}"

    # คืนค่า HttpResponse เสมอ โดยส่ง cart_items และ total_price ไปยังเทมเพลต
    return render(request, 'clothing/cart.html', {
        'cart_items': cart_items,
        'total_price': formatted_total_price
    })

# ฟังก์ชันอื่นๆ

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

# ฟังก์ชันค้นหาสินค้า
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
    favorite_objects = Favorite.objects.filter(user=request.user).select_related('clothing')
    favorite_clothes = [fav.clothing for fav in favorite_objects]
    return render(request, 'clothing/favorites_list.html', {'favorite_clothes': favorite_clothes})

# ฟังก์ชันเพิ่มสินค้าลงในรายการโปรด
@login_required
def add_to_favorites(request, pk):
    clothing_item = get_object_or_404(Clothing, pk=pk)
    if not Favorite.objects.filter(user=request.user, clothing=clothing_item).exists():
        Favorite.objects.create(user=request.user, clothing=clothing_item)
    return redirect('clothing:favorites_list')

# ฟังก์ชันสำหรับหน้าสถานะการจัดส่ง
def status(request):
    return render(request, 'clothing/status.html')


# ฟังก์ชันสำหรับหน้า profile
@login_required
def profile(request):
    return render(request, 'clothing/profile.html')

# ฟังก์ชันสำหรับการแก้ไขโปรไฟล์
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # สมมติว่าคุณมีฟอร์มที่ใช้งานสำหรับแก้ไขข้อมูลโปรไฟล์
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.profile.address = request.POST.get('address', user.profile.address)
        user.save()
        user.profile.save()
        return redirect('clothing:profile')
    
    return render(request, 'clothing/edit_profile.html', {'user': request.user})
# ฟังก์ชันสำหรับเปลี่ยนรหัสผ่าน
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)  # คำนึงถึง session หลังการเปลี่ยนรหัสผ่าน
            return redirect('clothing:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'clothing/change_password.html', {'form': form})