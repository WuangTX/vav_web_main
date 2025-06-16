from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Q
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid
from main.models import Product, ProductCategory, Project, ProjectTimeline, ProjectGallery, ContactMessage, News, NewsCategory
from .forms import ProductForm, CategoryForm, ProjectForm, ProjectTimelineForm, ProjectGalleryForm, NewsForm, NewsCategoryForm, ProjectGalleryMultipleForm

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
    total_news = News.objects.count()
    total_news_categories = NewsCategory.objects.count()
    new_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Project timeline statistics - simplified for workflow tracking
    active_projects = Project.objects.filter(
        timeline_entries__isnull=False
    ).distinct().count()
    
    # Recent timeline entries for projects
    recent_timeline_entries = ProjectTimeline.objects.select_related('project').order_by('-created_at')[:5]
    
    # Projects by status - count all timeline entries by status
    project_status_stats = {}
    for status, display in ProjectTimeline.STATUS_CHOICES:
        count = ProjectTimeline.objects.filter(status=status).count()
        project_status_stats[display] = count
    
    # News statistics
    published_news = News.objects.filter(status='published').count()
    draft_news = News.objects.filter(status='draft').count()
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_projects': total_projects,
        'total_news': total_news,
        'total_news_categories': total_news_categories,
        'published_news': published_news,
        'draft_news': draft_news,
        'new_messages': new_messages,
        'active_projects': active_projects,
        'recent_timeline_entries': recent_timeline_entries,
        'project_status_stats': project_status_stats,
        'recent_products': Product.objects.order_by('-created_at')[:5],
        'recent_projects': Project.objects.order_by('-created_at')[:5],
        'recent_news': News.objects.order_by('-created_at')[:5],
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
    messages_obj = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'dashboard/messages/list.html', {'messages_list': messages_obj})

@login_required
def message_detail(request, pk):
    """View to show message details and mark as read"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    # Mark as read when viewing
    if not message.is_read:
        message.is_read = True
        message.save()
    
    return render(request, 'dashboard/messages/detail.html', {'message': message})

@login_required
def message_delete(request, pk):
    """View to delete a message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Tin nhắn đã được xóa thành công.')
        return redirect('dashboard:message_list')
    
    return render(request, 'dashboard/messages/delete.html', {'message': message})

# Project Timeline management views
@login_required
def timeline_manage(request, project_id):
    """View to manage project timeline"""
    project = get_object_or_404(Project, id=project_id)
    timeline_entries = project.timeline_entries.all().order_by('order', 'created_at')
    
    context = {
        'project': project,
        'timeline_entries': timeline_entries,
    }
    return render(request, 'dashboard/projects/timeline_manage.html', context)

@login_required
def timeline_add(request, project_id):
    """View to add timeline entry"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectTimelineForm(request.POST)
        if form.is_valid():
            timeline = form.save(commit=False)
            timeline.project = project
            timeline.save()
            messages.success(request, 'Mốc thời gian đã được thêm thành công.')
            return redirect('dashboard:timeline_manage', project_id=project.id)
    else:
        form = ProjectTimelineForm(initial={'project': project})
        # Make project field readonly
        form.fields['project'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'project': project,
        'action': 'add'
    }
    return render(request, 'dashboard/projects/timeline_form.html', context)

@login_required
def timeline_edit(request, project_id, timeline_id):
    """View to edit timeline entry"""
    project = get_object_or_404(Project, id=project_id)
    timeline = get_object_or_404(ProjectTimeline, id=timeline_id, project=project)
    
    if request.method == 'POST':
        form = ProjectTimelineForm(request.POST, instance=timeline)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mốc thời gian đã được cập nhật.')
            return redirect('dashboard:timeline_manage', project_id=project.id)
    else:
        form = ProjectTimelineForm(instance=timeline)
        # Make project field readonly
        form.fields['project'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'project': project,
        'timeline': timeline,
        'action': 'edit'
    }
    return render(request, 'dashboard/projects/timeline_form.html', context)

@login_required
def timeline_delete(request, project_id, timeline_id):
    """View to delete timeline entry"""
    project = get_object_or_404(Project, id=project_id)
    timeline = get_object_or_404(ProjectTimeline, id=timeline_id, project=project)
    
    if request.method == 'POST':
        timeline.delete()
        messages.success(request, 'Mốc thời gian đã được xóa.')
        return redirect('dashboard:timeline_manage', project_id=project.id)
    
    context = {
        'project': project,
        'timeline': timeline,
    }
    return render(request, 'dashboard/projects/timeline_confirm_delete.html', context)

# Gallery Management Views
@login_required
def gallery_manage(request, project_id):
    """View to manage project gallery"""
    project = get_object_or_404(Project, id=project_id)
    gallery_images = project.gallery_images.all().order_by('order', 'created_at')
    
    context = {
        'project': project,
        'gallery_images': gallery_images,
    }
    return render(request, 'dashboard/projects/gallery_manage.html', context)

@login_required
def gallery_add(request, project_id):
    """View to add new gallery image"""
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = ProjectGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_image = form.save(commit=False)
            gallery_image.project = project
            gallery_image.save()
            messages.success(request, f'Ảnh đã được thêm vào thư viện dự án "{project.title}".')
            return redirect('dashboard:gallery_manage', project_id=project.id)
    else:
        form = ProjectGalleryForm(initial={'project': project})
        # Hide project field since it's pre-selected
        form.fields['project'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'project': project,
        'action': 'add',
    }
    return render(request, 'dashboard/projects/gallery_form.html', context)

@login_required
def gallery_edit(request, project_id, gallery_id):
    """View to edit gallery image"""
    project = get_object_or_404(Project, id=project_id)
    gallery_image = get_object_or_404(ProjectGallery, id=gallery_id, project=project)
    
    if request.method == 'POST':
        form = ProjectGalleryForm(request.POST, request.FILES, instance=gallery_image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ảnh trong thư viện đã được cập nhật.')
            return redirect('dashboard:gallery_manage', project_id=project.id)
    else:
        form = ProjectGalleryForm(instance=gallery_image)
        # Hide project field since it's pre-selected
        form.fields['project'].widget = forms.HiddenInput()
    
    context = {
        'form': form,
        'project': project,
        'gallery_image': gallery_image,
        'action': 'edit',
    }
    return render(request, 'dashboard/projects/gallery_form.html', context)

@login_required
def gallery_delete(request, project_id, gallery_id):
    """View to delete gallery image"""
    project = get_object_or_404(Project, id=project_id)
    gallery_image = get_object_or_404(ProjectGallery, id=gallery_id, project=project)
    
    if request.method == 'POST':
        gallery_image.delete()
        messages.success(request, 'Ảnh đã được xóa khỏi thư viện.')
        return redirect('dashboard:gallery_manage', project_id=project.id)
    
    context = {
        'project': project,
        'gallery_image': gallery_image,
    }
    return render(request, 'dashboard/projects/gallery_confirm_delete.html', context)


# News Management Views
@login_required
def news_list(request):
    """View to list all news"""
    news = News.objects.all().select_related('category').order_by('-created_at')
    return render(request, 'dashboard/news/list.html', {'news': news})


@login_required
@login_required
def news_add(request):
    """View to add new news"""
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tin tức đã được thêm thành công!')
            return redirect('dashboard:news_list')
        else:
            # Debug: Print form errors
            print("Form errors:", form.errors)
    else:
        form = NewsForm()
    
    return render(request, 'dashboard/news/form.html', {'form': form, 'action': 'add'})


@login_required
def news_edit(request, pk):
    """View to edit news"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tin tức đã được cập nhật!')
            return redirect('dashboard:news_list')
    else:
        form = NewsForm(instance=news)
    
    return render(request, 'dashboard/news/form.html', {'form': form, 'news': news, 'action': 'edit'})


@login_required
def news_delete(request, pk):
    """View to delete news"""
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        news.delete()
        messages.success(request, 'Tin tức đã được xóa!')
        return redirect('dashboard:news_list')
    
    return render(request, 'dashboard/news/confirm_delete.html', {'news': news})


# News Category Management Views
@login_required
def news_category_list(request):
    """View to list all news categories"""
    categories = NewsCategory.objects.all().order_by('name')
    return render(request, 'dashboard/news/category_list.html', {'categories': categories})


@login_required
def news_category_add(request):
    """View to add new news category"""
    if request.method == 'POST':
        form = NewsCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Danh mục tin tức đã được thêm thành công!')
            return redirect('dashboard:news_category_list')
    else:
        form = NewsCategoryForm()
    
    return render(request, 'dashboard/news/category_form.html', {'form': form, 'action': 'add'})


@login_required
def news_category_edit(request, pk):
    """View to edit news category"""
    category = get_object_or_404(NewsCategory, pk=pk)
    if request.method == 'POST':
        form = NewsCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Danh mục tin tức đã được cập nhật!')
            return redirect('dashboard:news_category_list')
    else:
        form = NewsCategoryForm(instance=category)
    
    return render(request, 'dashboard/news/category_form.html', {'form': form, 'category': category, 'action': 'edit'})


@login_required
def news_category_delete(request, pk):
    """View to delete news category"""
    category = get_object_or_404(NewsCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Danh mục tin tức đã được xóa!')
        return redirect('dashboard:news_category_list')
    
    return render(request, 'dashboard/news/category_confirm_delete.html', {'category': category})


@login_required
def upload_image(request):
    """View to handle image uploads for CKEditor"""
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if upload.content_type not in allowed_types:
            return JsonResponse({
                'error': 'Chỉ chấp nhận file ảnh (JPG, PNG, GIF, WebP)'
            }, status=400)
        
        # Validate file size (max 5MB)
        if upload.size > 5 * 1024 * 1024:
            return JsonResponse({
                'error': 'Kích thước file không được vượt quá 5MB'
            }, status=400)
        
        try:
            # Generate unique filename
            file_extension = os.path.splitext(upload.name)[1]
            unique_filename = f"news/content/{uuid.uuid4().hex}{file_extension}"
            
            # Save file
            file_path = default_storage.save(unique_filename, ContentFile(upload.read()))
            file_url = default_storage.url(file_path)
            
            return JsonResponse({
                'url': file_url
            })
            
        except Exception as e:
            return JsonResponse({
                'error': f'Lỗi khi upload file: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'error': 'Yêu cầu không hợp lệ'
    }, status=400)

@login_required
def project_gallery_multiple_add(request, project_id=None):
    """View to add multiple images to project gallery"""
    project = None
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        from .forms import ProjectGalleryMultipleForm
        form = ProjectGalleryMultipleForm(request.POST, request.FILES, project_id=project_id)
        
        if form.is_valid():
            try:
                gallery_items = form.save()
                messages.success(request, f'Đã thêm {len(gallery_items)} ảnh vào thư viện dự án thành công!')
                
                # Redirect to project detail or gallery list
                if project:
                    return redirect('dashboard:project_detail', id=project.id)
                else:
                    return redirect('dashboard:project_gallery_list')
                    
            except Exception as e:
                messages.error(request, f'Có lỗi xảy ra khi upload ảnh: {str(e)}')
        else:
            messages.error(request, 'Vui lòng kiểm tra lại thông tin!')
    else:
        from .forms import ProjectGalleryMultipleForm
        form = ProjectGalleryMultipleForm(project_id=project_id)
    
    context = {
        'form': form,
        'project': project,
        'title': f'Thêm nhiều ảnh - {project.title}' if project else 'Thêm nhiều ảnh vào thư viện dự án'
    }
    
    return render(request, 'dashboard/projects/gallery_multiple_add.html', context)

@login_required
def project_gallery_list(request):
    """View to list all project gallery images"""
    # Get all gallery items with related project info
    gallery_items = ProjectGallery.objects.select_related('project').order_by('project__title', 'order')
    
    # Filter by project if specified
    project_id = request.GET.get('project')
    if project_id:
        gallery_items = gallery_items.filter(project_id=project_id)
    
    # Get all projects for filter dropdown
    projects = Project.objects.all().order_by('title')
    
    context = {
        'gallery_items': gallery_items,
        'projects': projects,
        'selected_project_id': int(project_id) if project_id else None,
        'title': 'Quản lý thư viện ảnh dự án'
    }
    
    return render(request, 'dashboard/projects/gallery_list.html', context)

@login_required
def project_gallery_delete(request, id):
    """View to delete a project gallery image"""
    gallery_item = get_object_or_404(ProjectGallery, id=id)
    project_id = gallery_item.project.id
    
    if request.method == 'POST':
        try:
            # Delete the image file from storage
            if gallery_item.image:
                default_storage.delete(gallery_item.image.name)
            
            gallery_item.delete()
            messages.success(request, 'Đã xóa ảnh khỏi thư viện thành công!')
        except Exception as e:
            messages.error(request, f'Có lỗi xảy ra khi xóa ảnh: {str(e)}')
    
    return redirect('dashboard:project_detail', id=project_id)
