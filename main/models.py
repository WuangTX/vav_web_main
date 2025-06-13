from django.db import models
from django.utils.text import slugify
import os
import re
from datetime import datetime


def product_image_upload_to(instance, filename):
    """Generate upload path for product images using slug"""
    # Get file extension
    ext = filename.split('.')[-1].lower()
    
    # Validate file extension
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    if ext not in allowed_extensions:
        ext = 'jpg'  # Default to jpg if extension is not allowed
    
    # Create slug from product name
    slug = slugify(instance.name)
    
    # Remove any non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug)
    
    # Ensure slug is not empty
    if not slug:
        slug = 'product'
    
    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create new filename: slug_timestamp.extension
    new_filename = f"{slug}_{timestamp}.{ext}"
    
    return os.path.join('products/', new_filename)


def project_image_upload_to(instance, filename):
    """Generate upload path for project images using slug"""
    # Get file extension
    ext = filename.split('.')[-1].lower()
    
    # Validate file extension
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    if ext not in allowed_extensions:
        ext = 'jpg'  # Default to jpg if extension is not allowed
    
    # Create slug from project title
    slug = slugify(instance.title)
    
    # Remove any non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug)
    
    # Ensure slug is not empty
    if not slug:
        slug = 'project'
    
    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create new filename: slug_timestamp.extension
    new_filename = f"{slug}_{timestamp}.{ext}"
    
    return os.path.join('projects/', new_filename)


def project_gallery_upload_to(instance, filename):
    """Generate upload path for project gallery images using slug"""
    # Get file extension
    ext = filename.split('.')[-1].lower()
    
    # Validate file extension
    allowed_extensions = ['jpg', 'jpeg', 'png', 'webp', 'gif']
    if ext not in allowed_extensions:
        ext = 'jpg'  # Default to jpg if extension is not allowed
    
    # Create slug from project title
    slug = slugify(instance.project.title)
    
    # Remove any non-alphanumeric characters except hyphens
    slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug)
    
    # Ensure slug is not empty
    if not slug:
        slug = 'project'
    
    # Add timestamp to avoid conflicts
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create new filename: slug_gallery_timestamp.extension
    new_filename = f"{slug}_gallery_{timestamp}.{ext}"
    
    return os.path.join('projects/gallery/', new_filename)

class ProductCategory(models.Model):
    """Model for product categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Product Categories"

class Product(models.Model):
    """Model for furniture products"""
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=product_image_upload_to)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Product.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Project(models.Model):
    """Model for furniture projects/portfolio"""
    PROJECT_TYPES = (
        ('villa', 'Biệt Thự'),
        ('apartment', 'Căn Hộ'),
        ('office', 'Văn Phòng'),
        ('hotel', 'Khách Sạn'),
        ('restaurant', 'Nhà Hàng'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to=project_image_upload_to)
    completed_date = models.DateField()
    client = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Handle duplicate slugs
            original_slug = self.slug
            counter = 1
            while Project.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class ProjectTimeline(models.Model):
    """Model for simple project workflow steps"""
    STATUS_CHOICES = (
        ('consultation', 'Tư Vấn & Thiết Kế'),
        ('planning', 'Lập Kế Hoạch & Vật Liệu'),
        ('production', 'Sản Xuất & Chế Tác'),
        ('installation', 'Thi Công & Lắp Đặt'),
        ('completion', 'Nghiệm Thu & Bàn Giao'),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timeline_entries')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['project', 'order', 'created_at']
        
    def __str__(self):
        return f"{self.project.title} - {self.get_status_display()}"

class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


class ProjectGallery(models.Model):
    """Model for project gallery images"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery_images")
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=project_gallery_upload_to)
    order = models.PositiveIntegerField(default=0, help_text="Order to display images")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.project.title} - {self.title if self.title else 'Image'} {self.id}"
    
    class Meta:
        verbose_name_plural = "Project Gallery Images"
        ordering = ['order', 'created_at']
