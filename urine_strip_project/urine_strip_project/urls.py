from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('strip_analyzer.urls')),  # Include app URLs here
]
