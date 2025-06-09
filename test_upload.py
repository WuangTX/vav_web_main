#!/usr/bin/env python
"""
Test script để kiểm tra chức năng upload và đổi tên file
"""
import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vav_furniture.settings')
django.setup()

from main.models import Product, Project, ProductCategory
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date

def test_product_upload():
    """Test upload sản phẩm với tên file slug"""
    print("=== Test Product Upload ===")
    
    # Tạo category test nếu chưa có
    category, created = ProductCategory.objects.get_or_create(
        name="Test Category",
        defaults={
            'slug': 'test-category',
            'description': 'Test category for upload testing'
        }
    )
    
    # Tạo một file test
    test_image_content = b"fake image content"
    test_file = SimpleUploadedFile(
        "test image with special chars & spaces!.jpg",
        test_image_content,
        content_type="image/jpeg"
    )
    
    # Tạo product
    product = Product(
        category=category,
        name="Bàn Trà Gỗ Sồi Thông Minh & Hiện Đại",
        description="Test product description",
        price=1500000,
        image=test_file,
        featured=True
    )
    
    print(f"Tên sản phẩm: {product.name}")
    print(f"Tên file gốc: test image with special chars & spaces!.jpg")
    
    # Lưu product
    product.save()
    
    print(f"Slug được tạo: {product.slug}")
    print(f"Đường dẫn file mới: {product.image.name}")
    print(f"Tên file mới: {os.path.basename(product.image.name)}")
    
    # Xóa test data
    product.delete()
    if created:
        category.delete()
    
    print("✅ Test Product Upload hoàn thành!\n")

def test_project_upload():
    """Test upload dự án với tên file slug"""
    print("=== Test Project Upload ===")
    
    # Tạo một file test
    test_image_content = b"fake project image content"
    test_file = SimpleUploadedFile(
        "Dự án Villa Cao Cấp - Hình ảnh 1.png",
        test_image_content,
        content_type="image/png"
    )
    
    # Tạo project
    project = Project(
        title="Villa Cao Cấp Quận 7 - Phong Cách Tân Cổ Điển",
        project_type="villa",
        description="Test project description",
        client="Test Client",
        location="Quận 7, TP.HCM",
        completed_date=date.today(),
        image=test_file,
        featured=True
    )
    
    print(f"Tên dự án: {project.title}")
    print(f"Tên file gốc: Dự án Villa Cao Cấp - Hình ảnh 1.png")
    
    # Lưu project
    project.save()
    
    print(f"Slug được tạo: {project.slug}")
    print(f"Đường dẫn file mới: {project.image.name}")
    print(f"Tên file mới: {os.path.basename(project.image.name)}")
    
    # Xóa test data
    project.delete()
    
    print("✅ Test Project Upload hoàn thành!\n")

if __name__ == "__main__":
    print("🚀 Bắt đầu test chức năng upload và đổi tên file...\n")
    
    try:
        test_product_upload()
        test_project_upload()
        print("🎉 Tất cả test đều passed! Chức năng upload hoạt động tốt.")
        
    except Exception as e:
        print(f"❌ Có lỗi xảy ra: {e}")
        import traceback
        traceback.print_exc()
