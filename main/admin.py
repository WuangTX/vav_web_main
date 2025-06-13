from django.contrib import admin
from .models import ProductCategory, Product, Project, ProjectGallery, ProjectTimeline, ContactMessage


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
