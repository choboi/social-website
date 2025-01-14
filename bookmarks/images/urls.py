from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='image_create'),
    path('<int:id>/<slug:slug>/', views.image_detail, name='detail'),
    path('like/', views.image_like, name='like'),
    path('', views.image_list, name='list'),
    # ... other URL patterns ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
