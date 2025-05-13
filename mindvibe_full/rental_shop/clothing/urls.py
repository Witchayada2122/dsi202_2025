from django.urls import path
from . import views

app_name = 'clothing'  # ใช้ app_name ในการอ้างอิง URL

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('clothing/', views.clothing_list, name='clothing_list'),
    path('clothing/<int:pk>/', views.clothing_detail, name='clothing_detail'),
    path('search/', views.search_clothing, name='search_clothing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]
