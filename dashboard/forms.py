from django import forms
from django.db import models
from main.models import Product, ProductCategory, Project, ProjectTimeline, ProjectGallery, News, NewsCategory

class CategoryForm(forms.ModelForm):
    """Form for product category"""
    class Meta:
        model = ProductCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductForm(forms.ModelForm):
    """Form for product"""
    class Meta:
        model = Product
        fields = ['category', 'name', 'slug', 'description', 'price', 'image', 'featured']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectForm(forms.ModelForm):
    """Form for project"""
    class Meta:
        model = Project
        fields = ['title', 'slug', 'project_type', 'description', 'image', 
                 'completed_date', 'client', 'location', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'completed_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectTimelineForm(forms.ModelForm):
    """Form for simple project timeline"""
    class Meta:
        model = ProjectTimeline
        fields = ['project', 'status', 'title', 'description', 'order']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all().order_by('title')
        # If editing existing timeline, make project field readonly
        if self.instance.pk:
            self.fields['project'].widget.attrs['readonly'] = True

class ProjectGalleryForm(forms.ModelForm):
    """Form for project gallery"""
    class Meta:
        model = ProjectGallery
        fields = ['project', 'title', 'image', 'order']
        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tiêu đề ảnh (tùy chọn)'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': 0,
                'placeholder': 'Thứ tự hiển thị'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.all().order_by('title')
        
        # If editing existing gallery, make project field readonly
        if self.instance.pk:
            self.fields['project'].widget.attrs['readonly'] = True
            
        # Make title field optional but encourage its use
        self.fields['title'].required = False
        self.fields['title'].help_text = "Tiêu đề mô tả cho ảnh này (khuyến khích điền)"


class NewsCategoryForm(forms.ModelForm):
    """Form for news category"""
    class Meta:
        model = NewsCategory
        fields = ['name', 'slug', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên danh mục'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL slug (tự động tạo nếu để trống)'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Mô tả danh mục'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['slug'].required = False
        self.fields['description'].required = False


class NewsForm(forms.ModelForm):
    """Form for news article"""
    class Meta:
        model = News
        fields = [
            'category', 'title', 'slug', 'summary', 'content', 'image', 
            'image_position', 'image_caption', 'external_link', 'external_link_text',
            'tags', 'featured', 'status', 'author', 'published_at'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề bài viết'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL slug (tự động tạo nếu để trống)'}),
            'summary': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Tóm tắt ngắn gọn về bài viết (tối đa 500 ký tự)',
                'maxlength': 500
            }),            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 15, 
                'placeholder': 'Nội dung chi tiết của bài viết...',
                'style': 'display: none;'  # Hide the original textarea
            }),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'image_position': forms.Select(attrs={'class': 'form-control'}),
            'image_caption': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Chú thích cho hình ảnh (tùy chọn)'
            }),
            'external_link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://example.com'
            }),
            'external_link_text': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Văn bản hiển thị cho liên kết'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'thẻ1, thẻ2, thẻ3 (phân cách bằng dấu phẩy)'
            }),
            'featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-control', 
                'type': 'datetime-local'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional
        self.fields['slug'].required = False
        self.fields['image_caption'].required = False
        self.fields['external_link'].required = False
        self.fields['external_link_text'].required = False
        self.fields['tags'].required = False
        self.fields['published_at'].required = False
        
        # Set helpful help texts
        self.fields['image_position'].help_text = "Chọn vị trí hiển thị hình ảnh trong bài viết"
        self.fields['external_link'].help_text = "Link tham khảo hoặc nguồn tin (tùy chọn)"
        self.fields['tags'].help_text = "Các thẻ giúp phân loại bài viết, phân cách bằng dấu phẩy"
        self.fields['featured'].help_text = "Đánh dấu là tin nổi bật"
        self.fields['published_at'].help_text = "Để trống sẽ tự động lấy thời gian hiện tại khi xuất bản"

class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget for multiple file upload"""
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    """Custom field for multiple file upload"""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        kwargs.setdefault("help_text", "Chọn nhiều ảnh cùng lúc (Ctrl/Cmd + Click)")
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProjectGalleryMultipleForm(forms.Form):
    """Form for uploading multiple images to project gallery"""
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Dự án"
    )
    images = MultipleFileField(
        label="Chọn nhiều ảnh",
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*',
            'multiple': True
        })
    )
    
    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        
        # If project_id is provided, pre-select it and make it readonly
        if project_id:
            self.fields['project'].initial = project_id
            self.fields['project'].widget.attrs['readonly'] = True
            
        self.fields['project'].queryset = Project.objects.all().order_by('title')
        
    def save(self, commit=True):
        """Save multiple images to project gallery"""
        if not commit:
            return None
            
        project = self.cleaned_data['project']
        images = self.cleaned_data['images']
        
        # Get the current highest order for this project
        last_order = ProjectGallery.objects.filter(project=project).aggregate(
            max_order=models.Max('order')
        )['max_order'] or 0
        
        gallery_items = []
        for i, image in enumerate(images):
            gallery_item = ProjectGallery(
                project=project,
                image=image,
                title=f"Ảnh {last_order + i + 1}",
                order=last_order + i + 1
            )
            if commit:
                gallery_item.save()
            gallery_items.append(gallery_item)
            
        return gallery_items
