# Note về Lỗi URLs

Khi chạy dự án, có thể gặp lỗi liên quan đến URL patterns. Nguyên nhân có thể là do circular import hoặc cấu trúc URL không đúng.

## Cách Khắc Phục

1. Kiểm tra file `main/urls.py` và đảm bảo `urlpatterns` được khai báo đúng:
   ```python
   from django.urls import path
   from . import views
   
   urlpatterns = [
       path('', views.home, name='home'),
       path('about/', views.about, name='about'),
       path('products/', views.products, name='products'),
       path('projects/', views.projects, name='projects'),
       path('contact/', views.contact, name='contact'),
   ]
   ```

2. Kiểm tra file `vav_furniture/urls.py` và đảm bảo include đúng:
   ```python
   from django.contrib import admin
   from django.urls import path, include
   from django.conf import settings
   from django.conf.urls.static import static
   
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('', include('main.urls')),
   ]
   
   if settings.DEBUG:
       urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```

3. Kiểm tra xem không có circular import trong các file views.py, urls.py và models.py.

4. Nếu vẫn gặp vấn đề, có thể tạm thời comment phần include URLs trong file `vav_furniture/urls.py` để tạo migrations trước:
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       # path('', include('main.urls')),  # Comment tạm thời để tạo migrations
   ]
   ```

5. Sau khi đã tạo migrations thành công, có thể bỏ comment phần trên và chạy lại server.

## Cách Chạy Dự Án

1. Chạy file `run_server.bat` để thiết lập database và chạy server
2. Hoặc chạy các lệnh sau theo thứ tự:
   ```
   python manage.py makemigrations main
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
