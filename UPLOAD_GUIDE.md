# Hướng Dẫn Upload Ảnh Với Tên File Slug

## Tổng Quan
Hệ thống đã được cấu hình để tự động đổi tên file ảnh thành slug khi admin thêm sản phẩm hoặc dự án. Điều này giúp:

- **SEO tốt hơn**: Tên file có ý nghĩa, thân thiện với search engine
- **Quản lý dễ dàng**: Tên file dễ đọc và tìm kiếm
- **Tránh xung đột**: Tự động thêm timestamp để tránh trùng tên
- **Bảo mật**: Loại bỏ các ký tự đặc biệt có thể gây lỗi

## Cách Hoạt Động

### 1. Khi Upload Sản Phẩm (Product)
- **Input**: Tên sản phẩm = "Bàn Trà Gỗ Sồi Thông Minh & Hiện Đại"
- **File gốc**: "IMG_1234.jpg"
- **Output**: "ban-tra-go-soi-thong-minh-hien-ai_20250609_114718.jpg"

### 2. Khi Upload Dự Án (Project)  
- **Input**: Tiêu đề dự án = "Villa Cao Cấp Quận 7 - Phong Cách Tân Cổ Điển"
- **File gốc**: "photo.png"
- **Output**: "villa-cao-cap-quan-7-phong-cach-tan-co-ien_20250609_114718.png"

## Quy Tắc Đặt Tên

### 1. Tạo Slug
- Chuyển đổi từ tiếng Việt có dấu sang không dấu
- Thay khoảng trắng bằng dấu gạch ngang (-)
- Chuyển về chữ thường
- Loại bỏ ký tự đặc biệt

### 2. Thêm Timestamp
- Format: YYYYMMDD_HHMMSS
- Ví dụ: 20250609_114718 (9/6/2025 lúc 11:47:18)

### 3. Giữ Nguyên Extension
- Hỗ trợ: jpg, jpeg, png, webp, gif
- Mặc định: jpg (nếu extension không hợp lệ)

## Cấu Trúc Thư Mục

```
media/
├── products/
│   ├── ban-tra-go-soi-thong-minh_20250609_114718.jpg
│   ├── tu-quan-ao-hien-dai_20250609_120000.png
│   └── ...
├── projects/
│   ├── villa-cao-cap-quan-7_20250609_114718.jpg
│   ├── can-ho-penthouse-q1_20250609_120000.png
│   └── ...
```

## Sử Dụng Trong Admin

### 1. Thêm Sản Phẩm Mới
1. Vào Django Admin > Products > Add Product
2. Nhập tên sản phẩm (VD: "Ghế Sofa Da Thật Cao Cấp")
3. Slug sẽ tự động được tạo: "ghe-sofa-da-that-cao-cap"
4. Upload ảnh với tên bất kỳ
5. Ảnh sẽ được lưu với tên: "ghe-sofa-da-that-cao-cap_[timestamp].jpg"

### 2. Thêm Dự Án Mới
1. Vào Django Admin > Projects > Add Project  
2. Nhập tiêu đề dự án (VD: "Thiết Kế Nội Thất Khách Sạn 5 Sao")
3. Slug sẽ tự động được tạo: "thiet-ke-noi-that-khach-san-5-sao"
4. Upload ảnh với tên bất kỳ
5. Ảnh sẽ được lưu với tên: "thiet-ke-noi-that-khach-san-5-sao_[timestamp].jpg"

## Tự Động Tạo Slug

Nếu admin không nhập slug thủ công, hệ thống sẽ tự động:

1. **Tạo slug từ tên/tiêu đề**
2. **Kiểm tra trùng lặp**: Nếu slug đã tồn tại, thêm số (-1, -2, -3...)
3. **Lưu vào database**

## Test Chức Năng

Để test chức năng, chạy file test:

```bash
cd vav_web_main
python test_upload.py
```

## Lưu Ý Quan Trọng

1. **Backup**: Luôn backup dữ liệu trước khi thay đổi
2. **File cũ**: Các file ảnh cũ sẽ không bị ảnh hưởng
3. **Performance**: Tên file ngắn gọn giúp load trang nhanh hơn
4. **SEO**: Tên file có ý nghĩa giúp Google index tốt hơn

## Troubleshooting

### Lỗi Upload File
- Kiểm tra MEDIA_ROOT trong settings.py
- Đảm bảo thư mục media/ có quyền ghi
- Kiểm tra dung lượng file (thường < 5MB)

### Slug Trùng Lặp  
- Hệ thống tự động thêm số để tránh trùng
- VD: "ban-tra-go", "ban-tra-go-1", "ban-tra-go-2"

### File Extension Không Hỗ Trợ
- File sẽ được đổi extension thành .jpg
- Nên upload đúng định dạng: jpg, png, webp

---

**Phiên bản**: 1.0  
**Cập nhật**: 09/06/2025  
**Tác giả**: VAV Furniture Development Team
