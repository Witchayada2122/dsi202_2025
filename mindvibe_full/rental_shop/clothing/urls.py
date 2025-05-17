from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views



app_name = 'clothing'

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('clothing/', views.clothing_list, name='clothing_list'),
    path('clothing/<int:pk>/', views.clothing_detail, name='clothing_detail'),
    path('search/', views.search_clothing, name='search_clothing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('add_to_favorites/<int:pk>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:pk>/', views.remove_from_favorites_view, name='remove_from_favorites'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:pk>/<int:days>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.payment, name='payment'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('status/', views.status, name='status'),
    path('admin/update-status/<int:payment_id>/', views.update_order_status, name='update_order_status'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
]
