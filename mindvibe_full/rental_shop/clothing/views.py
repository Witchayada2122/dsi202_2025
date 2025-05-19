from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from .models import Clothing, Favorite, ClothingType
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import CustomUserCreationForm
from .models import Payment
from .models import OrderStatus
from django.db.models import Max
import hashlib




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
    type_filter = request.GET.get('type', '')

    clothes = Clothing.objects.all()

    if search_query:
        clothes = clothes.filter(name__icontains=search_query)

    if type_filter:
        clothes = clothes.filter(clothing_type__name__iexact=type_filter)

    clothing_types = ClothingType.objects.all()

    context = {
        'clothes': clothes,
        'search_query': search_query,
        'type_filter': type_filter,
        'clothing_types': clothing_types,
    }
    return render(request, 'clothing/clothing_list.html', context)

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
# ฟังก์ชันสำหรับหน้า signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # บันทึกผู้ใช้ใหม่
            login(request, user)  # ทำการล็อกอินให้ผู้ใช้ใหม่ทันทีหลังจากสมัครเสร็จ
            return redirect('clothing:clothing_list')  # ไปที่หน้า clothing_list หรือหน้าอื่น ๆ ตามต้องการ
    else:
        form = UserCreationForm()  # ถ้าไม่ใช่ POST ก็แค่แสดงฟอร์มเปล่า

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
                # แทนที่จะใช้ next หรือ LOGIN_REDIRECT_URL ให้ redirect ไปที่ clothing_list เสมอ
                return redirect('clothing:clothing_list')
    else:
        form = AuthenticationForm()
    next_url = request.GET.get('next')
    return render(request, 'clothing/login.html', {'form': form, 'next': next_url})

def get_gravatar_url(email, size=100):
    email_lower = email.strip().lower()
    hash_email = hashlib.md5(email_lower.encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash_email}?s={size}&d=identicon"

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


def remove_from_favorites_view(request, pk):
    try:
        # ค้นหาไอเทมในรายการโปรดที่ตรงกับ primary key (pk) ของสินค้า
        favorite_item = Favorite.objects.get(user=request.user, clothing_id=pk)
        favorite_item.delete()  # ลบสินค้าออกจากรายการโปรด
    except Favorite.DoesNotExist:
        # ถ้าสินค้าที่จะลบไม่มีอยู่ในรายการโปรดให้แสดงข้อผิดพลาด
        pass
    # หลังจากลบแล้วให้รีไดเรกต์กลับไปยังหน้ารายการโปรด
    return redirect('clothing:favorites_list')

# ฟังก์ชันสำหรับหน้าสถานะการจัดส่ง
def status(request):
    return render(request, 'clothing/status.html')


# ฟังก์ชันสำหรับหน้า profile
@login_required
def profile(request):
    user = request.user
    payments = Payment.objects.filter(user=user).order_by('-payment_date')
    status_dict = {}
    for payment in payments:
        latest_status = payment.statuses.order_by('-updated_at').first()
        status_dict[payment.id] = latest_status
    latest_payment = payments.first()

    gravatar_url = get_gravatar_url(user.email, size=150)

    if request.method == 'POST':
        # ... (เหมือนเดิม)
        pass

    context = {
        'user': user,
        'payments': payments,
        'status_dict': status_dict,
        'latest_payment': latest_payment,
        'gravatar_url': gravatar_url,
    }
    return render(request, 'clothing/profile.html', context)

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


# ฟังก์ชันสำหรับดึงข้อมูลสินค้าจากตะกร้า
def get_cart_items(request):
    cart = request.session.get('cart', [])
    cart_items = []
    
    for item in cart:
        try:
            product = get_object_or_404(Clothing, pk=item['product_id'])
            days = item.get('days', 1)  # จำนวนวันจาก cart
            # เลือกฟิลด์ราคาตามจำนวนวัน
            if days == 1:
                price = product.price_per_day_1
            elif days == 3:
                price = product.price_per_day_3
            elif days == 5:
                price = product.price_per_day_5
            elif days == 7:
                price = product.price_per_day_7
            else:
                price = product.price_per_day_1  # ค่าเริ่มต้นหาก days ไม่ถูกต้อง
            
            total_price = price * item['quantity']
            price_per_unit = total_price / item['quantity'] if item['quantity'] else 0

            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'days': days,
                'total': total_price,
                'price_per_unit': price_per_unit  # คำนวณราคาเฉลี่ยต่อหน่วย
            })
        except (KeyError, Clothing.DoesNotExist):
            continue
    return cart_items

# ฟังก์ชันสำหรับการเพิ่มสินค้าในตะกร้า
def add_to_cart(request, pk):
    clothing = get_object_or_404(Clothing, pk=pk)
    
    if request.method == 'POST':
        days = int(request.POST.get('days', 1))
        action = request.POST.get('action')
        quantity = 1  # ตั้งค่า quantity เป็น 1 โดยอัตโนมัติ
        
        cart = request.session.get('cart', [])
        
        # ตรวจสอบว่ามีสินค้าในตะกร้าแล้วหรือไม่ ถ้ามีเพิ่มจำนวน
        for item in cart:
            if item['product_id'] == clothing.pk and item['days'] == days:
                item['quantity'] += quantity
                break
        else:
            # ถ้าไม่มีสินค้าในตะกร้า ให้เพิ่มสินค้าใหม่
            cart.append({
                'product_id': clothing.pk,
                'quantity': quantity,
                'days': days
            })

        # บันทึกตะกร้าใน session
        request.session['cart'] = cart
        request.session.modified = True

        # Redirect ตาม action
        if action == 'buy_now':
            return redirect('clothing:payment')
        return redirect('clothing:cart')
    
    # หากไม่ใช่ POST ให้ redirect กลับไปที่ clothing_detail
    return redirect('clothing:clothing_detail', pk=pk)

def update_cart(request, pk):
    clothing = get_object_or_404(Clothing, pk=pk)
    cart = request.session.get('cart', [])
    quantity = int(request.POST.get('quantity', 1))
    days = int(request.POST.get('days', 1))

    updated = False
    for item in cart:
        if item['product_id'] == pk:
            item['quantity'] = quantity
            item['days'] = days
            updated = True
            break

    if not updated:
        cart.append({'product_id': pk, 'quantity': quantity, 'days': days})

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('clothing:cart')

# เพิ่มฟังก์ชันลบสินค้าออกจากตะกร้า
def remove_from_cart(request, pk, days):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if not (item['product_id'] == pk and item['days'] == days)]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('clothing:cart')

# ฟังก์ชันสำหรับหน้าตะกร้าสินค้า
def cart(request):
    cart_items = get_cart_items(request)
    total_price = sum(item['total'] for item in cart_items)
    return render(request, 'clothing/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price  # เป็น float หรือ Decimal
    })

# ฟังก์ชันสำหรับหน้าชำระเงิน
def payment(request):
    cart_items = get_cart_items(request)
    total_price = sum(item['total'] for item in cart_items)  # เป็นตัวเลข (Decimal หรือ float)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        proof = request.FILES.get('payment_proof')

        Payment.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone_number=phone_number,
            proof=proof,
            total_price=total_price
        )
        return redirect('clothing:status')

    return render(request, 'clothing/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price  # ส่งเป็นตัวเลขเลย
    })


@login_required
def status(request):
    payment = Payment.objects.filter(user=request.user).last()
    timeline = OrderStatus.objects.filter(payment=payment).order_by('-updated_at') if payment else []

    if request.method == 'POST':
        return_proof = request.FILES.get('return_proof')
        return_item_code = request.POST.get('return_item_code')
        if payment:
            payment.return_proof = return_proof
            payment.return_item_code = return_item_code
            payment.save()
            OrderStatus.objects.create(
                payment=payment,
                status='returned',
                updated_by=request.user,
                note='ลูกค้าส่งคืนสินค้าแล้ว'
            )
        return redirect('clothing:status')

    return render(request, 'clothing/status.html', {'order': payment, 'timeline': timeline})

# ✅ เพิ่มฟังก์ชันสำหรับ admin หรือพนักงานอัปเดตสถานะคำสั่งซื้อ
@login_required
def update_order_status(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)

    if request.method == 'POST':
        status_value = request.POST.get('status')
        tracking_number = request.POST.get('tracking_number')
        note = request.POST.get('note')

        OrderStatus.objects.create(
            payment=payment,
            status=status_value,
            tracking_number=tracking_number,
            updated_by=request.user,
            note=note
        )
        return redirect('clothing:update_order_status', payment_id=payment.id)

    all_statuses = OrderStatus.objects.filter(payment=payment).order_by('-updated_at')
    return render(request, 'clothing/admin_update_status.html', {
        'payment': payment,
        'statuses': all_statuses
    })
