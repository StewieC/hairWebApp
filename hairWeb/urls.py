from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('tips/', include('tips.urls')),
    path('shop/', include('shop.urls')),
    path('booking/', include('booking.urls')),  
    path('ai_chat/',include('ai_chat.urls')),
]

# ← ADD THESE TWO LINES AT THE END
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)