from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.generic import TemplateView

def home(request):
    return JsonResponse({"status": "success", "data": "AgriBot API Running"})

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/disease/', include('disease.urls')),
    path('api/chat/', include('chat.urls')),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login-page'),
    path('predict/', TemplateView.as_view(template_name='predict.html'), name='predict-page'),
    path('chat/', TemplateView.as_view(template_name='chat.html'), name='chat-page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
