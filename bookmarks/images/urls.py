from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='image_create'),
    path('detail/<int:id>/<slug:slug>/', views.image_detail, name='image_detail'),
    path('images/<int:image_id>/detail/<slug:image_slug>/', views.image_detail, name='detail'),
    # ... other URL patterns ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
