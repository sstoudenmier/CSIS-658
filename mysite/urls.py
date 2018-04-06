from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('atm/', include('atm.urls')),
    path('admin/', admin.site.urls),
]
