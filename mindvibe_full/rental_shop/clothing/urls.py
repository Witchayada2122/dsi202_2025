from django.urls import path
from . import views

app_name = 'clothing'

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('clothing/', views.clothing_list, name='clothing_list'),
    path('clothing/<int:pk>/', views.clothing_detail, name='clothing_detail'),
    path('search/', views.search_clothing, name='search_clothing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('cart/', views.cart, name='cart'),  # หน้าตะกร้า
    path('payment/', views.payment, name='payment'),  # หน้าชำระเงิน
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('status/', views.status, name='status'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
]
