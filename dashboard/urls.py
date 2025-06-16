from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication URLs
    path('login/', views.dashboard_login, name='login'),
    path('logout/', views.dashboard_logout, name='logout'),
    
    # Dashboard main page
    path('', views.dashboard_home, name='home'),
    
    # Product management
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
    # Product Category management
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Project management
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.project_add, name='project_add'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),    # Project Timeline management
    path('projects/<int:project_id>/timeline/', views.timeline_manage, name='timeline_manage'),
    path('projects/<int:project_id>/timeline/add/', views.timeline_add, name='timeline_add'),
    path('projects/<int:project_id>/timeline/<int:timeline_id>/edit/', views.timeline_edit, name='timeline_edit'),
    path('projects/<int:project_id>/timeline/<int:timeline_id>/delete/', views.timeline_delete, name='timeline_delete'),
      # Project Gallery management
    path('projects/<int:project_id>/gallery/', views.gallery_manage, name='gallery_manage'),
    path('projects/<int:project_id>/gallery/add/', views.gallery_add, name='gallery_add'),
    path('projects/<int:project_id>/gallery/<int:gallery_id>/edit/', views.gallery_edit, name='gallery_edit'),
    path('projects/<int:project_id>/gallery/<int:gallery_id>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # Multiple images upload for project gallery
    path('projects/gallery/multiple-add/', views.project_gallery_multiple_add, name='project_gallery_multiple_add'),
    path('projects/<int:project_id>/gallery/multiple-add/', views.project_gallery_multiple_add, name='project_gallery_multiple_add_with_project'),
    path('projects/gallery/', views.project_gallery_list, name='project_gallery_list'),
    path('projects/gallery/<int:id>/delete/', views.project_gallery_delete, name='project_gallery_delete'),
      # Contact messages management
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    path('messages/delete/<int:pk>/', views.message_delete, name='message_delete'),
    
    # News management
    path('news/', views.news_list, name='news_list'),
    path('news/add/', views.news_add, name='news_add'),
    path('news/edit/<int:pk>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:pk>/', views.news_delete, name='news_delete'),
      # News Category management
    path('news/categories/', views.news_category_list, name='news_category_list'),
    path('news/categories/add/', views.news_category_add, name='news_category_add'),
    path('news/categories/edit/<int:pk>/', views.news_category_edit, name='news_category_edit'),
    path('news/categories/delete/<int:pk>/', views.news_category_delete, name='news_category_delete'),
    
    # CKEditor image upload
    path('upload-image/', views.upload_image, name='upload_image'),
]
