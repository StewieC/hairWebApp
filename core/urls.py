# core/urls.py
from django.urls import path
from .views import HomeView, quiz_submit, quiz_result, ai_hair_chat

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('quiz/submit/', quiz_submit, name='quiz_submit'),
    path('quiz/result/', quiz_result, name='quiz_result'),
    path('ai-chat/', ai_hair_chat, name='ai_hair_chat'),
]