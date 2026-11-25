# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/pagos/', include('apps.payments.urls')),
    path('api/sync/', include('apps.sync.urls')),
]