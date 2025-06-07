from django.shortcuts import render, get_object_or_404
from .models import Product, ProductCategory, Project, ContactMessage
from django.db.models import Q

def home(request):
    """View for the home page"""
    featured_products = Product.objects.filter(featured=True)[:4]
    featured_projects = Project.objects.filter(featured=True)[:3]
    
    context = {
        'featured_products': featured_products,
        'featured_projects': featured_projects,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """View for the about page"""
    return render(request, 'main/about.html')

def products(request):
    """View for the products page"""
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)
    
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
    products = Product.objects.filter(category=category)
    categories = ProductCategory.objects.all()
    
    context = {
        'category': category,
        'products': products,
        'categories': categories,
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
    
    context = {
        'project': project,
        'related_projects': related_projects,
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
