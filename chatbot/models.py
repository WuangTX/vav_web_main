from django.db import models
from django.contrib.auth.models import User
from main.models import Product, Project


class ChatSession(models.Model):
    """Model để lưu phiên chat của khách hàng"""
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Chat Session {self.session_id}"
    
    class Meta:
        ordering = ['-updated_at']


class ChatMessage(models.Model):
    """Model để lưu tin nhắn trong chat"""
    MESSAGE_TYPES = (
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Metadata cho recommendations
    recommended_products = models.ManyToManyField(Product, blank=True, related_name='chat_recommendations')
    recommended_projects = models.ManyToManyField(Project, blank=True, related_name='chat_recommendations')
    
    def __str__(self):
        return f"{self.session.session_id} - {self.message_type}: {self.content[:50]}"
    
    class Meta:
        ordering = ['created_at']


class ChatFeedback(models.Model):
    """Model để lưu feedback từ khách hàng"""
    RATING_CHOICES = (
        (1, 'Rất không hài lòng'),
        (2, 'Không hài lòng'),
        (3, 'Bình thường'),
        (4, 'Hài lòng'),
        (5, 'Rất hài lòng'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.session.session_id} - Rating: {self.rating}"
