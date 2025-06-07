# VAV Furniture - Website Doanh Nghiệp Nội Thất

Dự án website giới thiệu doanh nghiệp nội thất VAV Furniture được xây dựng trên nền tảng Django.

## Tính Năng

- **Trang Chủ**: Giới thiệu tổng quan về VAV Furniture với banner lớn, các mục giới thiệu về dịch vụ, sản phẩm nổi bật và dự án tiêu biểu.
- **Giới Thiệu**: Thông tin chi tiết về công ty, đội ngũ nhân viên, tầm nhìn và sứ mệnh.
- **Sản Phẩm**: Trưng bày các sản phẩm nội thất theo danh mục, với dữ liệu động từ cơ sở dữ liệu.
- **Chi Tiết Sản Phẩm**: Trang hiển thị thông tin chi tiết về từng sản phẩm.
- **Dự Án**: Giới thiệu các dự án nội thất đã thực hiện, có thể lọc theo loại dự án.
- **Chi Tiết Dự Án**: Trang hiển thị thông tin chi tiết về từng dự án.
- **Liên Hệ**: Form liên hệ hoạt động đầy đủ, thông tin liên lạc và bản đồ.
- **Tìm Kiếm**: Chức năng tìm kiếm sản phẩm.

## Cấu Trúc Dự Án

```
vav_furniture_main/
│
├── main/                           # Ứng dụng Django chính
│   ├── migrations/                 # Các file migration cơ sở dữ liệu
│   ├── __init__.py
│   ├── admin.py                    # Cấu hình trang admin
│   ├── apps.py                     # Cấu hình ứng dụng
│   ├── models.py                   # Mô hình dữ liệu
│   ├── tests.py                    # Unit tests
│   ├── urls.py                     # URL routing cho ứng dụng main
│   └── views.py                    # Views xử lý logic
│
├── media/                          # Thư mục lưu trữ hình ảnh upload
│   ├── products/                   # Hình ảnh sản phẩm
│   └── projects/                   # Hình ảnh dự án
│
├── static/                         # Thư mục lưu trữ static files
│   ├── css/                        # File CSS
│   ├── images/                     # Hình ảnh tĩnh
│   ├── js/                         # JavaScript
│   └── lib/                        # Thư viện bên thứ ba
│
├── templates/                      # Thư mục chứa templates
│   ├── base.html                   # Template cơ sở
│   └── main/                       # Templates của ứng dụng main
│       ├── home.html               # Trang chủ
│       ├── about.html              # Trang giới thiệu
│       ├── products.html           # Trang sản phẩm
│       ├── product_detail.html     # Trang chi tiết sản phẩm
│       ├── projects.html           # Trang dự án
│       ├── project_detail.html     # Trang chi tiết dự án
│       └── contact.html            # Trang liên hệ
│
├── vav_furniture/                  # Thư mục cấu hình Django project
│   ├── __init__.py
│   ├── asgi.py                     # ASGI config
│   ├── settings.py                 # Cài đặt dự án
│   ├── urls.py                     # URL routing chính
│   └── wsgi.py                     # WSGI config
│
├── image_requirements.md           # Hướng dẫn về yêu cầu hình ảnh
├── url_error_fix.md                # Hướng dẫn khắc phục lỗi URL
├── README.md                       # Tài liệu hướng dẫn này
├── manage.py                       # Công cụ quản lý Django
└── run_server.bat                  # Script chạy server
```

## Mô Hình Dữ Liệu

- **ProductCategory**: Danh mục sản phẩm với tên, slug và mô tả
- **Product**: Sản phẩm nội thất với tên, mô tả, giá, hình ảnh, danh mục
- **Project**: Dự án nội thất đã thực hiện với tiêu đề, loại dự án, mô tả, hình ảnh
- **ContactMessage**: Lưu trữ tin nhắn từ form liên hệ

## Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- pip (công cụ quản lý gói của Python)
- Trình duyệt web hiện đại (Chrome, Firefox, Edge, Safari)

### Cài Đặt

1. Sao chép dự án:
   ```bash
   git clone <repository-url>
   cd vav_furniture_main
   ```

2. Cài đặt các gói phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

3. Chạy file thiết lập:
   ```bash
   run_server.bat
   ```
   Script này sẽ:
   - Tạo migrations cho cơ sở dữ liệu
   - Áp dụng migrations
   - Tạo tài khoản admin (nếu chưa có)
     - Username: admin
     - Password: adminpassword
   - Khởi động development server

4. Truy cập website tại http://127.0.0.1:8000/
5. Truy cập trang quản trị tại http://127.0.0.1:8000/admin/

## Quản Lý Nội Dung

### Thêm Sản Phẩm

1. Đăng nhập vào trang quản trị
2. Điều hướng đến phần "Products"
3. Nhấp vào "Add Product"
4. Điền thông tin sản phẩm và tải lên hình ảnh
5. Đánh dấu "Featured" nếu muốn sản phẩm xuất hiện ở trang chủ

### Thêm Dự Án

1. Đăng nhập vào trang quản trị
2. Điều hướng đến phần "Projects"
3. Nhấp vào "Add Project"
4. Điền thông tin dự án và tải lên hình ảnh
5. Đánh dấu "Featured" nếu muốn dự án xuất hiện ở trang chủ

### Quản Lý Tin Nhắn Liên Hệ

1. Đăng nhập vào trang quản trị
2. Điều hướng đến phần "Contact Messages"
3. Xem và quản lý các tin nhắn đã nhận

## Tùy Chỉnh Hình Ảnh

Để biết thông tin chi tiết về yêu cầu hình ảnh, xem tài liệu [Image Requirements](image_requirements.md).

## Triển Khai Production

Để triển khai lên môi trường production, cần cân nhắc:

1. Tạo file `.env` để lưu trữ các biến môi trường nhạy cảm (SECRET_KEY, DATABASE_URL, v.v.)
2. Cài đặt các cài đặt production trong `settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   
   # Sử dụng cơ sở dữ liệu PostgreSQL
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'vav_furniture',
           'USER': 'your_username',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

3. Thiết lập phục vụ static và media files:
   ```python
   # Static files
   STATIC_ROOT = BASE_DIR / 'staticfiles'
   
   # Media files
   MEDIA_ROOT = BASE_DIR / 'mediafiles'
   ```

4. Sử dụng WSGI server như Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn vav_furniture.wsgi:application
   ```

5. Thiết lập web server (Nginx/Apache) để proxy các request đến Gunicorn và phục vụ static/media files.

6. Thiết lập HTTPS với chứng chỉ SSL (sử dụng Let's Encrypt).

7. Thiết lập đường dẫn tĩnh cho email:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.example.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your_email@example.com'
   EMAIL_HOST_PASSWORD = 'your_password'
   DEFAULT_FROM_EMAIL = 'VAV Furniture <your_email@example.com>'
   ```

## Tính Năng Tương Lai

1. Tài khoản người dùng và chức năng yêu thích/wishlist
2. Đặt hàng trực tuyến và tích hợp thanh toán
3. Phần blog cho mẹo thiết kế và chăm sóc nội thất
4. Lọc và tìm kiếm nâng cao cho sản phẩm
5. Hỗ trợ đa ngôn ngữ
6. Đăng ký nhận bản tin

## Xử Lý Sự Cố

Nếu gặp lỗi URL pattern, tham khảo tài liệu [URL Error Fix](url_error_fix.md).

## Liên Hệ

Để được hỗ trợ, vui lòng liên hệ [thông tin liên hệ].
│   └── wsgi.py                     # WSGI config
│
├── manage.py                       # File quản lý Django
└── image_requirements.md           # Hướng dẫn về hình ảnh cần có
```

## Cài Đặt và Chạy

1. Cài đặt Python và Django:
   ```bash
   pip install django pillow
   ```

2. Clone repository:
   ```bash
   git clone <repository-url>
   cd vav_furniture_main
   ```

3. Tạo và apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Tạo superuser để quản lý trang admin:
   ```bash
   python manage.py createsuperuser
   ```

5. Chạy server development:
   ```bash
   python manage.py runserver
   ```

6. Truy cập website tại:
   - Frontend: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Các Thành Phần Cần Bổ Sung

1. **Hình Ảnh**:
   - Tham khảo file `image_requirements.md` để biết danh sách các hình ảnh cần có cho website.

2. **Dữ Liệu**:
   - Thêm dữ liệu thực tế về sản phẩm, dự án và các thông tin khác thông qua trang admin.

3. **Chức Năng Nâng Cao**:
   - Tích hợp blog/tin tức
   - Hệ thống đặt hàng/báo giá
   - Đăng ký nhận thông tin qua email
   - Tích hợp mạng xã hội

## Tùy Chỉnh Giao Diện

- Các file CSS và JavaScript nằm trong thư mục `static/`
- Các templates nằm trong thư mục `templates/`

## Lưu Ý

- Chế độ `DEBUG = True` chỉ nên dùng trong môi trường phát triển
- Đảm bảo cập nhật `SECRET_KEY` trước khi triển khai lên môi trường production
- Cấu hình thêm cài đặt bảo mật và hiệu suất cho môi trường production

## Tác Giả

VAV Furniture Team
