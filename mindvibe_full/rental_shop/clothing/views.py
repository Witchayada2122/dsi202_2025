from django.shortcuts import render, get_object_or_404
from .models import Clothing
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate

# หน้า Welcome
def welcome(request):
    return render(request, 'clothing/welcome.html')

# หน้าแสดงรายการเสื้อผ้า
def clothing_list(request):
    # รับค่าจากการค้นหาชื่อ (search) และสี (color)
    search_query = request.GET.get('search', '')  # คำค้นหาจากช่องค้นหาชื่อ
    color_filter = request.GET.get('color', '')  # ค่าที่เลือกจากตัวเลือกสี

    # กรองสินค้าตามชื่อและสี
    clothes = Clothing.objects.all()

    if search_query:
        clothes = clothes.filter(name__icontains=search_query)  # ค้นหาจากชื่อสินค้าตามคำค้น

    if color_filter:
        clothes = clothes.filter(color__iexact=color_filter)  # ค้นหาจากสี

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

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # หลังจากสมัครเสร็จให้ไปหน้า login
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('clothing_list')  # หากล็อกอินสำเร็จจะพาไปหน้ารายการสินค้า
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

