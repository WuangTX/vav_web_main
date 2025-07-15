# SEO Sitemap Generator for VAV Furniture
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from main.models import Product, Project, News

class StaticViewSitemap(Sitemap):
    """Sitemap for static pages"""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return ['home', 'about', 'products', 'projects', 'news_list', 'contact']
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()

class ProductSitemap(Sitemap):
    """Sitemap for products"""
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else timezone.now()
    
    def location(self, obj):
        return f'/products/{obj.slug}/'

class ProjectSitemap(Sitemap):
    """Sitemap for projects"""
    changefreq = "monthly"
    priority = 0.7
    
    def items(self):
        return Project.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else timezone.now()
    
    def location(self, obj):
        return f'/projects/{obj.slug}/'

class NewsSitemap(Sitemap):
    """Sitemap for news"""
    changefreq = "weekly"
    priority = 0.6
    
    def items(self):
        return News.objects.filter(status='published').order_by('-created_at')
    
    def lastmod(self, obj):
        return obj.updated_at if hasattr(obj, 'updated_at') else obj.created_at
    
    def location(self, obj):
        return f'/news/{obj.slug}/'

# Sitemap dictionary for registration
sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
    'projects': ProjectSitemap,
    'news': NewsSitemap,
}
