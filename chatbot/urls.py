from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot_page, name='chat_page'),
    path('api/chat/', views.ChatView.as_view(), name='chat_api'),
    path('api/feedback/', views.feedback_view, name='feedback_api'),
]
