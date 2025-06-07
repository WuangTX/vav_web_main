from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from main.models import Product, ProductCategory, Project, ContactMessage
from .forms import ProductForm, CategoryForm, ProjectForm

def dashboard_login(request):
    """View for custom admin login page"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    
    return render(request, 'dashboard/login.html')

@login_required
def dashboard_logout(request):
    """View to handle admin logout"""
    logout(request)
    return redirect('dashboard:login')

@login_required
def dashboard_home(request):
    """View for dashboard home page"""
    total_products = Product.objects.count()
    total_categories = ProductCategory.objects.count()
    total_projects = Project.objects.count()
    new_messages = ContactMessage.objects.filter(is_read=False).count()
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_projects': total_projects,
        'new_messages': new_messages,
        'recent_products': Product.objects.order_by('-created_at')[:5],
        'recent_projects': Project.objects.order_by('-created_at')[:5],
        'recent_messages': ContactMessage.objects.filter(is_read=False).order_by('-created_at')[:5],
    }
    
    return render(request, 'dashboard/home.html', context)

# Product management views
@login_required
def product_list(request):
    """View to list all products"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'dashboard/products/list.html', {'products': products})

@login_required
def product_add(request):
    """View to add a new product"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sản phẩm đã được thêm thành công.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': 'Thêm Sản Phẩm Mới'})

@login_required
def product_edit(request, pk):
    """View to edit a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sản phẩm đã được cập nhật thành công.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'dashboard/products/form.html', {'form': form, 'title': 'Chỉnh Sửa Sản Phẩm', 'product': product})

@login_required
def product_delete(request, pk):
    """View to delete a product"""
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Sản phẩm đã được xóa thành công.')
        return redirect('dashboard:product_list')
    
    return render(request, 'dashboard/products/delete.html', {'product': product})

# Category management views
@login_required
def category_list(request):
    """View to list all product categories"""
    categories = ProductCategory.objects.all()
    return render(request, 'dashboard/categories/list.html', {'categories': categories})

@login_required
def category_add(request):
    """View to add a new product category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Danh mục đã được thêm thành công.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'dashboard/categories/form.html', {'form': form, 'title': 'Thêm Danh Mục Mới'})

@login_required
def category_edit(request, pk):
    """View to edit a product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Danh mục đã được cập nhật thành công.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'dashboard/categories/form.html', {'form': form, 'title': 'Chỉnh Sửa Danh Mục', 'category': category})

@login_required
def category_delete(request, pk):
    """View to delete a product category"""
    category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Danh mục đã được xóa thành công.')
        return redirect('dashboard:category_list')
    
    return render(request, 'dashboard/categories/delete.html', {'category': category})

# Project management views
@login_required
def project_list(request):
    """View to list all projects"""
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'dashboard/projects/list.html', {'projects': projects})

@login_required
def project_add(request):
    """View to add a new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dự án đã được thêm thành công.')
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm()
    
    return render(request, 'dashboard/projects/form.html', {'form': form, 'title': 'Thêm Dự Án Mới'})

@login_required
def project_edit(request, pk):
    """View to edit a project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dự án đã được cập nhật thành công.')
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'dashboard/projects/form.html', {'form': form, 'title': 'Chỉnh Sửa Dự Án', 'project': project})

@login_required
def project_delete(request, pk):
    """View to delete a project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Dự án đã được xóa thành công.')
        return redirect('dashboard:project_list')
    
    return render(request, 'dashboard/projects/delete.html', {'project': project})

# Contact message management views
@login_required
def message_list(request):
    """View to list all contact messages"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'dashboard/messages/list.html', {'messages_list': messages_list})

@login_required
def message_detail(request, pk):
    """View to show message details and mark as read"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    # Mark message as read if it hasn't been read yet
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'dashboard/messages/detail.html', {'message': message})

@login_required
def message_delete(request, pk):
    """View to delete a contact message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Tin nhắn đã được xóa thành công.')
        return redirect('dashboard:message_list')
    
    return render(request, 'dashboard/messages/delete.html', {'message': message})
