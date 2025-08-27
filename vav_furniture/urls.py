"""
URL configuration for vav_furniture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.decorators.http import require_GET
import os

import os

# Import sitemaps
try:
    from sitemaps import sitemaps
except ImportError:
    sitemaps = {}

@require_GET
def robots_txt(request):
    """Serve robots.txt file"""
    robots_path = os.path.join(settings.BASE_DIR, 'robots.txt')
    try:
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/plain')
    except FileNotFoundError:
        # Fallback robots.txt content
        content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/

Sitemap: {}/sitemap.xml""".format(request.build_absolute_uri('/'))
        return HttpResponse(content, content_type='text/plain')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('', include('main.urls')),
    
    # SEO URLs
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Custom error pages
handler403 = 'main.views.custom_403'
handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'

# Add media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Test error pages in development
    urlpatterns += [
        path('403/', TemplateView.as_view(template_name='403.html'), name='403'),
        path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
    ]
