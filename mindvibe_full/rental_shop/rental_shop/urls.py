# rental_shop/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clothing.urls')),  # เส้นทางไปยังแอป clothing
]

# เพิ่มการให้บริการไฟล์สื่อ (media) ในระหว่างการพัฒนา

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
