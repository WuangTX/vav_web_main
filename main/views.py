from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Project, ContactMessage, News, NewsCategory
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    """View for the home page"""
    featured_products = Product.objects.filter(featured=True)[:8]
    featured_projects = Project.objects.filter(featured=True)[:3]
    featured_news = News.objects.filter(featured=True, status='published')[:3]
    
    context = {
        'featured_products': featured_products,
        'featured_projects': featured_projects,
        'featured_news': featured_news,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """View for the about page"""
    return render(request, 'main/about.html')

def products(request):
    """View for the products page"""
    products_list = Product.objects.all()
    categories = ProductCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query) | products_list.filter(description__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'main/products.html', context)

def product_detail(request, slug):
    """View for the product detail page"""
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'main/product_detail.html', context)

def products_by_category(request, category_slug):
    """View to filter products by category"""
    category = get_object_or_404(ProductCategory, slug=category_slug)
    products_list = Product.objects.filter(category=category)
    categories = ProductCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products_list = products_list.filter(name__icontains=search_query) | products_list.filter(description__icontains=search_query)
    
    # Pagination
    paginator = Paginator(products_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'main/products.html', context)

def projects(request):
    """View for the projects showcase page"""
    projects = Project.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(client__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'projects': projects,
        'search_query': search_query,
    }
    return render(request, 'main/projects.html', context)

def project_detail(request, slug):
    """View for the project detail page"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(project_type=project.project_type).exclude(id=project.id)[:3]
    
    # Get gallery images for the project, ordered by order field
    gallery_images = project.gallery_images.all().order_by('order', 'created_at')
    
    # Get timeline entries for the project, ordered by order and creation date
    timeline_entries = project.timeline_entries.all().order_by('order', 'created_at')
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'gallery_images': gallery_images,
        'timeline_entries': timeline_entries,
    }
    return render(request, 'main/project_detail.html', context)

def contact(request):
    """View for the contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the contact message
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        
        # Add a success message
        success = True
        context = {'success': success}
        return render(request, 'main/contact.html', context)
    
    return render(request, 'main/contact.html')


def news_list(request):
    """View for the news list page"""
    news_list = News.objects.filter(status='published').select_related('category')
    categories = NewsCategory.objects.all()
    
    # Filter by category
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(NewsCategory, slug=category_slug)
        news_list = news_list.filter(category=category)
    else:
        category = None
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
      # Pagination
    paginator = Paginator(news_list, 3)  # 3 news articles per page
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Featured news for sidebar
    featured_news = News.objects.filter(status='published', featured=True)[:5]
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'featured_news': featured_news,
    }
    return render(request, 'main/news_list.html', context)


def news_detail(request, slug):
    """View for the news detail page"""
    news = get_object_or_404(News, slug=slug, status='published')
    
    # Increment view count
    news.views += 1
    news.save(update_fields=['views'])
    
    # Related news from same category
    related_news = News.objects.filter(
        category=news.category, 
        status='published'
    ).exclude(id=news.id)[:4]
    
    # Recent news for sidebar
    recent_news = News.objects.filter(status='published').exclude(id=news.id)[:5]
    
    context = {
        'news': news,
        'related_news': related_news,
        'recent_news': recent_news,
    }
    return render(request, 'main/news_detail.html', context)


def news_by_category(request, category_slug):
    """View to filter news by category"""
    category = get_object_or_404(NewsCategory, slug=category_slug)
    news_list = News.objects.filter(category=category, status='published')
    categories = NewsCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(summary__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__icontains=search_query)
        )
      # Pagination
    paginator = Paginator(news_list, 3)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # Featured news for sidebar
    featured_news = News.objects.filter(status='published', featured=True)[:5]
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
        'featured_news': featured_news,
    }
    return render(request, 'main/news_list.html', context)
