from django.urls import path
from .views import ai_hair_chat

urlpatterns = [
    path('', ai_hair_chat, name='ai_hair_chat'),
]