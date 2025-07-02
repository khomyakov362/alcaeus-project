from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls', namespace='books')),
    path('users/', include('users.urls', namespace='users')),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
