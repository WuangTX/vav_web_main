from django.db import migrations, transaction
from django.utils.text import slugify
from datetime import date

def create_sample_data(apps, schema_editor):
    ProductCategory = apps.get_model('main', 'ProductCategory')
    Product = apps.get_model('main', 'Product')
    Project = apps.get_model('main', 'Project')
    
    # Create Product Categories
    categories = [
        {'name': 'Phòng Khách', 'description': 'Nội thất cho phòng khách: sofa, bàn trà, kệ tivi, ...'},
        {'name': 'Phòng Ngủ', 'description': 'Nội thất cho phòng ngủ: giường, tủ quần áo, bàn trang điểm, ...'},
        {'name': 'Phòng Ăn', 'description': 'Nội thất cho phòng ăn: bàn ăn, ghế ăn, tủ rượu, ...'},
        {'name': 'Văn Phòng', 'description': 'Nội thất văn phòng: bàn làm việc, ghế văn phòng, tủ tài liệu, ...'},
        {'name': 'Nhà Bếp', 'description': 'Nội thất nhà bếp: tủ bếp, đảo bếp, ...'},
    ]
    
    category_objects = {}
    for cat in categories:
        slug = slugify(cat['name'])
        category = ProductCategory.objects.create(
            name=cat['name'],
            slug=slug,
            description=cat['description']
        )
        category_objects[slug] = category
    
    # Create Sample Products (without images because we can't upload them in this script)
    products = [
        {
            'name': 'Sofa Da Cao Cấp', 
            'category': category_objects['phong-khach'],
            'description': 'Sofa da cao cấp nhập khẩu từ Ý, thiết kế hiện đại với chất liệu da bò thật 100%.', 
            'price': 25000000, 
            'featured': True
        },
        {
            'name': 'Bàn Trà Mặt Đá', 
            'category': category_objects['phong-khach'],
            'description': 'Bàn trà mặt đá cẩm thạch, chân kim loại mạ vàng sang trọng.', 
            'price': 12000000, 
            'featured': False
        },
        {
            'name': 'Giường Ngủ Gỗ Óc Chó', 
            'category': category_objects['phong-ngu'],
            'description': 'Giường ngủ được làm từ gỗ óc chó cao cấp, thiết kế sang trọng và bền đẹp.', 
            'price': 35000000, 
            'featured': True
        },
        {
            'name': 'Tủ Quần Áo 4 Cánh', 
            'category': category_objects['phong-ngu'],
            'description': 'Tủ quần áo 4 cánh với thiết kế hiện đại, nhiều ngăn chứa tiện dụng.', 
            'price': 18000000, 
            'featured': False
        },
        {
            'name': 'Bàn Ăn Mở Rộng', 
            'category': category_objects['phong-an'],
            'description': 'Bàn ăn có thể mở rộng, phù hợp cho cả gia đình nhỏ và tiệc gia đình đông người.', 
            'price': 15000000, 
            'featured': True
        },
        {
            'name': 'Bàn Làm Việc Thông Minh', 
            'category': category_objects['van-phong'],
            'description': 'Bàn làm việc với nhiều ngăn kéo và kệ đựng tài liệu, thiết kế ngăn nắp và tiện dụng.', 
            'price': 8500000, 
            'featured': True
        },
    ]
    
    for prod in products:
        slug = slugify(prod['name'])
        Product.objects.create(
            name=prod['name'],
            slug=slug,
            category=prod['category'],
            description=prod['description'],
            price=prod['price'],
            featured=prod['featured'],
            # Image is required, but we can't upload it in this script
            # We'll use a placeholder and update later
            image='products/placeholder.jpg'
        )
    
    # Create Sample Projects
    projects = [
        {
            'title': 'Biệt Thự Vinhomes Central Park',
            'project_type': 'villa',
            'description': 'Thiết kế và thi công nội thất cho biệt thự 300m2 tại Vinhomes Central Park, phong cách hiện đại sang trọng.',
            'client': 'Gia đình anh Nguyễn Văn A',
            'location': 'TP. Hồ Chí Minh',
            'featured': True
        },
        {
            'title': 'Căn Hộ Masteri Thảo Điền',
            'project_type': 'apartment',
            'description': 'Thiết kế nội thất căn hộ 120m2 theo phong cách Scandinavian tinh tế và ấm cúng.',
            'client': 'Chị Trần Thị B',
            'location': 'TP. Hồ Chí Minh',
            'featured': True
        },
        {
            'title': 'Văn Phòng Công Ty ABC',
            'project_type': 'office',
            'description': 'Thiết kế và thi công nội thất văn phòng 500m2 hiện đại, chuyên nghiệp.',
            'client': 'Công ty ABC',
            'location': 'Hà Nội',
            'featured': True
        },
    ]
    
    for proj in projects:
        slug = slugify(proj['title'])
        Project.objects.create(
            title=proj['title'],
            slug=slug,
            project_type=proj['project_type'],
            description=proj['description'],
            client=proj['client'],
            location=proj['location'],
            featured=proj['featured'],
            # Image is required but we can't upload it here
            image='projects/placeholder.jpg',
            completed_date=date(2024, 1, 1) # Placeholder date
        )

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_data),
    ]
