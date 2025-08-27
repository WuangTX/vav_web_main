from django.contrib import admin
from .models import ProductCategory, Product, ProductDetailContent, Project, ProjectGallery, ProjectTimeline, ContactMessage, NewsCategory, News


class ProductDetailContentInline(admin.TabularInline):
    """Inline admin for product detail content"""
    model = ProductDetailContent
    extra = 1
    fields = ('content_type', 'title', 'content', 'image', 'image_caption', 'order')
    ordering = ['order']

class ProjectGalleryInline(admin.TabularInline):
    """Inline admin for project gallery images"""
    model = ProjectGallery
    extra = 3  # Number of empty forms to display
    fields = ('image', 'title', 'order')
    ordering = ['order']

class ProjectTimelineInline(admin.TabularInline):
    """Inline admin for project timeline"""
    model = ProjectTimeline
    extra = 1
    fields = ('status', 'title', 'description', 'order')
    ordering = ['order']

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'featured', 'created_at')
    list_filter = ('category', 'featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductDetailContentInline]

@admin.register(ProductDetailContent)
class ProductDetailContentAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'content_type', 'order', 'created_at')
    list_filter = ('content_type', 'product__category')
    search_fields = ('product__name', 'title', 'content')
    ordering = ['product', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'project_type', 'client', 'location', 'completed_date', 'featured')
    list_filter = ('project_type', 'featured')
    search_fields = ('title', 'description', 'client', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectGalleryInline, ProjectTimelineInline]

@admin.register(ProjectTimeline)
class ProjectTimelineAdmin(admin.ModelAdmin):
    list_display = ('project', 'status', 'title', 'order')
    list_filter = ('status',)
    search_fields = ('project__title', 'title', 'description')
    ordering = ['project', 'order']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    
    def has_add_permission(self, request):
        return False


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'featured', 'author', 'views', 'published_at')
    list_filter = ('status', 'category', 'featured', 'published_at', 'created_at')
    search_fields = ('title', 'summary', 'content', 'author', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'category', 'status', 'author')
        }),
        ('Nội dung', {
            'fields': ('summary', 'content', 'tags')
        }),
        ('Hình ảnh', {
            'fields': ('image', 'image_position', 'image_caption')
        }),
        ('Liên kết ngoài', {
            'fields': ('external_link', 'external_link_text'),
            'classes': ('collapse',)
        }),
        ('Cài đặt', {
            'fields': ('featured', 'published_at')
        }),
        ('Thống kê', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')
